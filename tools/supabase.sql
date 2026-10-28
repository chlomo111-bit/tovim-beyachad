-- טובעים ביחד : base de données complète (Supabase > SQL Editor > Run, une seule fois)
-- Remplacer MOT_DE_PASSE_A_CHANGER avant de lancer.

create extension if not exists pgcrypto with schema extensions;

-- ================= PASSAGERS =================
create table if not exists public.passengers (
  id          bigint generated always as identity primary key,
  handle      text not null unique check (handle ~ '^[a-z0-9._]{1,30}$'),
  vip         boolean not null default false,          -- a commenté = pont VIP
  style       jsonb   not null default '{}'::jsonb,    -- accessoires imposés par l'admin
  joined_ship int     not null default 0,              -- bateau sur lequel il est monté
  referred_by text,
  refs        int not null default 0,
  streak      int not null default 0,
  best_streak int not null default 0,
  last_visit  date,
  created_at  timestamptz not null default now()
);
alter table public.passengers enable row level security;
create policy "pass_read" on public.passengers for select using (true);

-- Paliers : 25 / 100 / 1 000 / 10 000 / 100 000 / 1 000 000
create or replace function public.ship_caps() returns int[] language sql immutable as $$ select array[25,100,1000,10000,100000,1000000] $$;
create or replace function public.ship_index(n bigint) returns int language sql immutable as $$
  select coalesce((select i - 1 from generate_subscripts(public.ship_caps(), 1) i where n < (public.ship_caps())[i] order by i limit 1), 5)
$$;

-- Naufrages : qui a fait couler quel bateau
create table if not exists public.sinks (
  ship_idx  int primary key,
  handle    text not null,
  sunk_at   timestamptz not null default now()
);
alter table public.sinks enable row level security;
create policy "sinks_read" on public.sinks for select using (true);

create or replace function public.after_passenger_insert() returns trigger
language plpgsql security definer set search_path = public as $$
declare n bigint; caps int[] := ship_caps(); i int;
begin
  select count(*) into n from passengers;
  for i in 1..array_length(caps,1) loop
    if n = caps[i] then
      insert into sinks(ship_idx, handle) values (i - 1, new.handle) on conflict do nothing;
    end if;
  end loop;
  return null;
end $$;
drop trigger if exists trg_after_passenger on public.passengers;
create trigger trg_after_passenger after insert on public.passengers for each row execute function public.after_passenger_insert();

-- Mot de passe admin
create table if not exists public.admin_secret (pass_hash text not null);
revoke all on public.admin_secret from anon, authenticated;
insert into public.admin_secret (pass_hash) values (extensions.crypt('MOT_DE_PASSE_A_CHANGER', extensions.gen_salt('bf')));

create or replace function public.is_admin(pass text) returns boolean
language sql security definer set search_path = public, extensions as $$
  select exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash))
$$;
revoke all on function public.is_admin(text) from public;

-- Ajout / mise à jour en liste (#admin)
create or replace function public.admin_upsert(pass text, items jsonb)
returns integer language plpgsql security definer set search_path = public, extensions as $$
declare n integer := 0; it jsonb; cur int;
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  for it in select * from jsonb_array_elements(items) loop
    if coalesce((it->>'remove')::boolean, false) then
      delete from passengers where handle = lower(it->>'handle');
    else
      select ship_index(count(*)) into cur from passengers;
      insert into passengers (handle, vip, style, joined_ship)
      values (lower(it->>'handle'), coalesce((it->>'vip')::boolean, false), coalesce(it->'style', '{}'::jsonb), cur)
      on conflict (handle) do update
        set vip   = coalesce((it->>'vip')::boolean, passengers.vip),
            style = passengers.style || excluded.style;
    end if;
    n := n + 1;
  end loop;
  return n;
end $$;
revoke all on function public.admin_upsert(text, jsonb) from public;
grant execute on function public.admin_upsert(text, jsonb) to anon, authenticated;

-- Inscription d'un joueur (avec parrain)
create or replace function public.join_passenger(h text, ref text default null)
returns setof public.passengers language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare hid text := lower(btrim(h)); r text := lower(btrim(coalesce(ref, ''))); cur int;
begin
  if hid !~ '^[a-z0-9._]{1,30}$' then raise exception 'bad_handle'; end if;
  if not exists (select 1 from passengers where passengers.handle = hid) then
    if r = '' or r = hid or not exists (select 1 from passengers where passengers.handle = r) then r := null; end if;
    select ship_index(count(*)) into cur from passengers;
    insert into passengers(handle, referred_by, joined_ship) values (hid, r, cur);
    if r is not null then update passengers set refs = refs + 1 where passengers.handle = r; end if;
  end if;
  return query select * from passengers where passengers.handle = hid;
end $$;
revoke all on function public.join_passenger(text, text) from public;
grant execute on function public.join_passenger(text, text) to anon, authenticated;

-- Série de jours
create or replace function public.check_in(h text)
returns table(streak int, best_streak int) language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare hid text := lower(btrim(h)); d date := (now() at time zone 'Asia/Jerusalem')::date; lv date; s int; b int;
begin
  select p.last_visit, p.streak, p.best_streak into lv, s, b from passengers p where p.handle = hid;
  if not found then return; end if;
  if lv is distinct from d then
    if lv = d - 1 then s := s + 1; else s := 1; end if;
    b := greatest(b, s);
    update passengers set last_visit = d, streak = s, best_streak = b where passengers.handle = hid;
  end if;
  return query select s, b;
end $$;
revoke all on function public.check_in(text) from public;
grant execute on function public.check_in(text) to anon, authenticated;

-- ================= BILLETS : 3 × 20 ₪ par jour, heures aléatoires espacées =================
create table if not exists public.billet_slots (
  day      date not null,
  slot     int  not null,
  opens_at timestamptz not null,
  prize    int not null default 20,
  primary key (day, slot)
);
alter table public.billet_slots enable row level security;
revoke all on public.billet_slots from anon, authenticated;

create table if not exists public.treasure_wins (
  day       date not null,
  slot      int  not null,
  handle    text not null check (handle ~ '^[a-z0-9._]{1,30}$'),
  found_at  timestamptz not null default now(),
  primary key (day, slot)
);
alter table public.treasure_wins enable row level security;
create policy "wins_read" on public.treasure_wins for select using (true);

create or replace function public.ensure_slots(d date) returns void
language plpgsql security definer set search_path = public as $$
begin
  if exists (select 1 from billet_slots where day = d) then return; end if;
  insert into billet_slots(day, slot, opens_at) values
   (d, 1, ((d + time '09:00') + make_interval(mins => floor(random()*150)::int)) at time zone 'Asia/Jerusalem'),
   (d, 2, ((d + time '13:00') + make_interval(mins => floor(random()*180)::int)) at time zone 'Asia/Jerusalem'),
   (d, 3, ((d + time '18:00') + make_interval(mins => floor(random()*210)::int)) at time zone 'Asia/Jerusalem')
  on conflict do nothing;
end $$;
revoke all on function public.ensure_slots(date) from public;

create or replace function public.billet_state(h text default '')
returns json language plpgsql security definer set search_path = public as $$
declare d date := (now() at time zone 'Asia/Jerusalem')::date; cur record; nx record; w record;
begin
  perform ensure_slots(d); perform ensure_slots(d + 1);
  select * into cur from billet_slots s where s.day = d and s.opens_at <= now() order by s.slot desc limit 1;
  select * into nx from billet_slots s where s.opens_at > now() order by s.opens_at limit 1;
  if cur.slot is not null then select t.handle, t.found_at into w from treasure_wins t where t.day = d and t.slot = cur.slot; end if;
  return json_build_object('day', d, 'slot', cur.slot, 'prize', coalesce(cur.prize, 20), 'opens_at', cur.opens_at,
    'next_at', nx.opens_at, 'next_prize', coalesce(nx.prize, 20), 'winner', w.handle, 'found_at', w.found_at, 'now', now());
end $$;
revoke all on function public.billet_state(text) from public;
grant execute on function public.billet_state(text) to anon, authenticated;

create or replace function public.claim_treasure(h text)
returns table(handle text, found_at timestamptz, is_me boolean)
language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare d date := (now() at time zone 'Asia/Jerusalem')::date; s int;
begin
  if not exists (select 1 from passengers p where p.handle = lower(h)) then raise exception 'not_a_passenger'; end if;
  select bs.slot into s from billet_slots bs where bs.day = d and bs.opens_at <= now() order by bs.slot desc limit 1;
  if s is null then raise exception 'no_billet'; end if;
  insert into treasure_wins(day, slot, handle) values (d, s, lower(h)) on conflict (day, slot) do nothing;
  return query select w.handle, w.found_at, w.handle = lower(h) from treasure_wins w where w.day = d and w.slot = s;
end $$;
revoke all on function public.claim_treasure(text) from public;
grant execute on function public.claim_treasure(text) to anon, authenticated;

-- ================= PIÈCES D'OR (activité quand on s'ennuie) =================
create table if not exists public.coins (
  handle  text primary key,
  total   int not null default 0,
  today   int not null default 0,
  day     date,
  last_at timestamptz not null default now()
);
alter table public.coins enable row level security;
create policy "coins_read" on public.coins for select using (true);

create or replace function public.add_coins(h text, n integer) returns json
language plpgsql security definer set search_path = public as $$
#variable_conflict use_variable
declare hid text := lower(btrim(h)); d date := (now() at time zone 'Asia/Jerusalem')::date; k int := least(greatest(coalesce(n,0),0),15); r record;
begin
  if not exists (select 1 from passengers p where p.handle = hid) then raise exception 'not_a_passenger'; end if;
  insert into coins(handle, total, today, day, last_at) values (hid, 0, 0, d, now() - interval '1 minute') on conflict (handle) do nothing;
  select * into r from coins x where x.handle = hid for update;
  if r.day is distinct from d then update coins x set today = 0, day = d where x.handle = hid; r.today := 0; end if;
  if r.last_at > now() - interval '2 seconds' then k := 0; end if;
  k := least(k, greatest(0, 1500 - r.today));
  update coins x set total = x.total + k, today = x.today + k, last_at = now() where x.handle = hid returning x.total, x.today into r.total, r.today;
  return json_build_object('total', r.total, 'today', r.today, 'added', k);
end $$;
revoke all on function public.add_coins(text, integer) from public;
grant execute on function public.add_coins(text, integer) to anon, authenticated;

-- ================= CHAT =================
create table if not exists public.messages (
  id          bigint generated always as identity primary key,
  handle      text not null,
  body        text not null check (char_length(body) between 1 and 140),
  created_at  timestamptz not null default now()
);
alter table public.messages enable row level security;
create policy "msg_read" on public.messages for select using (true);

create or replace function public.post_message(h text, body text)
returns bigint language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare hid text := lower(btrim(h)); b text := btrim(body); nid bigint;
begin
  if not exists (select 1 from passengers p where p.handle = hid) then raise exception 'not_a_passenger'; end if;
  if char_length(b) < 1 or char_length(b) > 140 then raise exception 'bad_length'; end if;
  if b ~* '(https?://|www\.)' then raise exception 'no_links'; end if;
  if exists (select 1 from messages m where m.handle = hid and m.created_at > now() - interval '10 seconds') then raise exception 'too_fast'; end if;
  insert into messages(handle, body) values (hid, b) returning id into nid;
  return nid;
end $$;
revoke all on function public.post_message(text, text) from public;
grant execute on function public.post_message(text, text) to anon, authenticated;

create or replace function public.admin_delete_message(pass text, mid bigint)
returns void language plpgsql security definer set search_path = public, extensions as $$
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  delete from messages where id = mid;
end $$;
revoke all on function public.admin_delete_message(text, bigint) from public;
grant execute on function public.admin_delete_message(text, bigint) to anon, authenticated;

-- ================= ACTUALITÉS + ÉVÉNEMENT DU JOUR =================
create table if not exists public.news (
  id          bigint generated always as identity primary key,
  title       text not null,
  body        text not null,
  created_at  timestamptz not null default now()
);
alter table public.news enable row level security;
create policy "news_read" on public.news for select using (true);

create or replace function public.admin_post_news(pass text, title text, body text)
returns bigint language plpgsql security definer set search_path = public, extensions as $$
#variable_conflict use_variable
declare nid bigint;
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  insert into news(title, body) values (title, body) returning id into nid;
  return nid;
end $$;
revoke all on function public.admin_post_news(text, text, text) from public;
grant execute on function public.admin_post_news(text, text, text) to anon, authenticated;

-- type : none / storm / shark / iceberg / party / whale / kraken
create table if not exists public.game_state (
  key   text primary key,
  value jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.game_state enable row level security;
create policy "state_read" on public.game_state for select using (true);
insert into public.game_state(key, value) values ('event', '{"type":"none"}') on conflict do nothing;

create or replace function public.admin_set_event(pass text, ev jsonb)
returns void language plpgsql security definer set search_path = public, extensions as $$
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  insert into game_state(key, value, updated_at) values ('event', ev, now())
  on conflict (key) do update set value = excluded.value, updated_at = now();
end $$;
revoke all on function public.admin_set_event(text, jsonb) from public;
grant execute on function public.admin_set_event(text, jsonb) to anon, authenticated;

-- ================= ACCÈS DU SITE =================
grant usage on schema public to anon, authenticated;
grant select on public.passengers, public.sinks, public.treasure_wins, public.coins, public.messages, public.news, public.game_state to anon, authenticated;

insert into public.news(title, body) values (
  'ברוכים הבאים לסיפון! 🚢',
  '🌊 המטרה של כולנו: להטביע את הספינה!
🧍 כל עוקב = נוסע. כל תגובה = כרטיס VIP ⭐
💸 3 שטרות של 20 ₪ מוסתרים על הסיפון כל יום
📣 הזמינו חברים עם הקישור האישי שלכם: כל חבר מקרב את הטביעה!'
);

-- ================= AUTOMATISATION INSTAGRAM (anti-doublon) =================
create table if not exists public.ig_seen_comments (comment_id text primary key, handle text not null, seen_at timestamptz not null default now());
create table if not exists public.ig_welcomed (handle text primary key, comment_id text, replied_at timestamptz not null default now());
alter table public.ig_seen_comments enable row level security;
alter table public.ig_welcomed enable row level security;
revoke all on public.ig_seen_comments from anon, authenticated;
revoke all on public.ig_welcomed from anon, authenticated;

-- ================= V2 (28.10.2026) : billets bloqués jusqu'au premier naufrage (25 passagers) =================
create or replace function public.billets_unlocked() returns boolean
language sql stable security definer set search_path = public as $$
  select exists(select 1 from sinks where ship_idx = 0) or (select count(*) from passengers) >= 25
$$;
revoke all on function public.billets_unlocked() from public;
-- billet_state renvoie {"locked":true,"need":N} tant que ce n'est pas débloqué ; claim_treasure refuse avec 'locked'
-- (et refuse le compte du jeu tovim_beyachad). Voir la version en ligne dans Supabase.
