-- טובעים ביחד : V3 (29.10.2026) — fonctions communes à tous les jeux de Shlomo
-- pièces par jour, missions du jour, boîte à idées, chat modéré (realtime), statistiques, classements.
-- Appliqué en ligne le 29.10.2026 (projet xcrlfujevlvwmrswwvfq). Ré-exécutable sans danger.

-- ================= 1. PIÈCES PAR JOUEUR ET PAR JOUR =================
create table if not exists public.coins_daily (
  handle text not null,
  day    date not null,
  coins  int  not null default 0,
  primary key (handle, day)
);
alter table public.coins_daily enable row level security;
revoke all on public.coins_daily from anon, authenticated;
insert into public.coins_daily(handle, day, coins)
  select handle, day, today from public.coins where day is not null and today > 0
  on conflict (handle, day) do update set coins = greatest(coins_daily.coins, excluded.coins);

-- crédit interne (pièces ramassées ou bonus de mission) : total + jour + historique
create or replace function public.credit_coins(hid text, k int) returns json
language plpgsql security definer set search_path = public as $$
#variable_conflict use_variable
declare d date := (now() at time zone 'Asia/Jerusalem')::date; r record;
begin
  insert into coins(handle, total, today, day, last_at) values (hid, 0, 0, d, now() - interval '1 minute') on conflict (handle) do nothing;
  update coins x set today = 0, day = d where x.handle = hid and x.day is distinct from d;
  update coins x set total = x.total + k, today = x.today + k where x.handle = hid returning x.total, x.today into r;
  insert into coins_daily(handle, day, coins) values (hid, d, k) on conflict (handle, day) do update set coins = coins_daily.coins + k;
  return json_build_object('total', r.total, 'today', r.today, 'added', k);
end $$;
revoke all on function public.credit_coins(text, int) from public, anon, authenticated;

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
  if k > 0 then
    insert into coins_daily(handle, day, coins) values (hid, d, k) on conflict (handle, day) do update set coins = coins_daily.coins + k;
  end if;
  return json_build_object('total', r.total, 'today', r.today, 'added', k);
end $$;
revoke all on function public.add_coins(text, integer) from public;
grant execute on function public.add_coins(text, integer) to anon, authenticated;

-- ================= 2. FILTRE DE MODÉRATION (chat + idées) =================
-- renvoie null si OK, sinon : link / phone / email / private / bad
create or replace function public.mod_check(body text) returns text
language plpgsql immutable set search_path = public as $$
declare b text := lower(coalesce(body,'')); flat text; sq text; w text; L constant text := '[^a-z0-9א-ת]';
begin
  -- liens
  if b ~ '(https?://|www\.|://)' or b ~ ('[a-z0-9-]{2,}\s*(\.|dot|נקודה)\s*(com|net|org|co|il|io|me|ly|gg|tv|app|xyz|info|link|site|online|ru|to)(' || L || '|$)') then return 'link'; end if;
  -- e-mails
  if b ~ '[a-z0-9._%+-]+@\s*[a-z0-9-]+\s*\.\s*[a-z]{2,}' or b ~ '(gmail|hotmail|walla|yahoo|outlook|icloud)' then return 'email'; end if;
  -- téléphones (7 chiffres ou plus, même séparés)
  if regexp_replace(b, '[\s\-\.\(\)\+_/]', '', 'g') ~ '[0-9]{7,}' then return 'phone'; end if;
  -- pas de messages privés / sortie vers d'autres apps
  if b ~ ('(whats ?app|וואטסאפ|ווטסאפ|וואצאפ|ווצאפ|טלגרם|telegram|snapchat|סנאפ|סנפצ|בפרטי|(^|' || L || ')(dm|pm|דיאם)(' || L || '|$)|תשלח(י)? לי הודעה|כתבו לי בפרטי)') then return 'private'; end if;
  -- insultes et contenus sexuels
  flat := regexp_replace(b, '[^a-z0-9א-ת]', '', 'g');
  sq := regexp_replace(flat, '(.)\1+', '\1', 'g');
  foreach w in array array['שרמוט','כוסאמ','כוסאחת','כוסעמ','בנזונ','בתזונ','מזדיי','תזדיי','לזיין','זיון','פורנו','סקס','fuck','fuk','bitch','cunt','porn','whore','slut','nigg','fagg','pusy','pussy','motherf','nude'] loop
    if position(w in flat) > 0 or position(w in sq) > 0 then return 'bad'; end if;
  end loop;
  foreach w in array array['זונה','זונות','זין','זיין','מניאק','מניאקית','ציצים','חרא','מפגר','מפגרת','שמוק','דביל','מטומטם','מטומטמת','קוקסינל','sex','sexy','ass','dick','cock','tits','boobs','shit','retard','nazi','נאצי','hitler','היטלר','תמות','תמותי'] loop
    if b ~ ('(^|' || L || ')[והשבלמכ]?' || w || '(' || L || '|$)') then return 'bad'; end if;
  end loop;
  return null;
end $$;

-- ================= 3. CHAT MODÉRÉ + SIGNALEMENTS + REALTIME =================
alter table public.messages add column if not exists hidden  boolean not null default false;
alter table public.messages add column if not exists reports int     not null default 0;
drop policy if exists "msg_read" on public.messages;
create policy "msg_read" on public.messages for select using (not hidden);

create table if not exists public.chat_reports (
  message_id bigint not null references public.messages(id) on delete cascade,
  reporter   text not null,
  created_at timestamptz not null default now(),
  primary key (message_id, reporter)
);
alter table public.chat_reports enable row level security;
revoke all on public.chat_reports from anon, authenticated;

create or replace function public.post_message(h text, body text)
returns bigint language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare hid text := lower(btrim(h)); b text := btrim(regexp_replace(body, '\s+', ' ', 'g')); nid bigint; why text;
begin
  if not exists (select 1 from passengers p where p.handle = hid) then raise exception 'not_a_passenger'; end if;
  if char_length(b) < 1 or char_length(b) > 140 then raise exception 'bad_length'; end if;
  why := mod_check(b);
  if why = 'link' then raise exception 'no_links'; elsif why is not null then raise exception 'mod_%', why; end if;
  if exists (select 1 from messages m where m.handle = hid and m.created_at > now() - interval '10 seconds') then raise exception 'too_fast'; end if;
  insert into messages(handle, body) values (hid, b) returning id into nid;
  return nid;
end $$;
revoke all on function public.post_message(text, text) from public;
grant execute on function public.post_message(text, text) to anon, authenticated;

create or replace function public.report_message(h text, mid bigint) returns json
language plpgsql security definer set search_path = public as $$
declare hid text := lower(btrim(coalesce(h,''))); n int; hid_ok boolean;
begin
  if not exists (select 1 from passengers p where p.handle = hid) then raise exception 'not_a_passenger'; end if;
  if exists (select 1 from messages m where m.id = mid and m.handle = hid) then raise exception 'own_message'; end if;
  insert into chat_reports(message_id, reporter) values (mid, hid) on conflict do nothing;
  if found then
    update messages set reports = reports + 1, hidden = hidden or reports + 1 >= 3 where id = mid returning reports, hidden into n, hid_ok;
  else
    select reports, hidden into n, hid_ok from messages where id = mid;
  end if;
  return json_build_object('reports', coalesce(n,0), 'hidden', coalesce(hid_ok,false));
end $$;
revoke all on function public.report_message(text, bigint) from public;
grant execute on function public.report_message(text, bigint) to anon, authenticated;

create or replace function public.admin_reported(pass text) returns setof public.messages
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  return query select * from messages where reports > 0 or hidden order by hidden desc, reports desc, id desc limit 50;
end $$;
revoke all on function public.admin_reported(text) from public;
grant execute on function public.admin_reported(text) to anon, authenticated;

create or replace function public.admin_restore_message(pass text, mid bigint) returns void
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not is_admin(pass) then raise exception 'bad password'; end if;
  delete from chat_reports where message_id = mid;
  update messages set hidden = false, reports = 0 where id = mid;
end $$;
revoke all on function public.admin_restore_message(text, bigint) from public;
grant execute on function public.admin_restore_message(text, bigint) to anon, authenticated;

do $$ begin
  if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'messages') then
    alter publication supabase_realtime add table public.messages;
  end if;
end $$;

-- ================= 4. BOÎTE À IDÉES =================
create table if not exists public.ideas (
  id         bigint generated always as identity primary key,
  handle     text not null,
  body       text not null check (char_length(body) between 1 and 200),
  status     text not null default 'new',   -- new / read
  created_at timestamptz not null default now()
);
alter table public.ideas enable row level security;
revoke all on public.ideas from anon, authenticated;

create or replace function public.submit_idea(h text, body text) returns json
language plpgsql security definer set search_path = public as $$
declare hid text := lower(btrim(coalesce(h,''))); b text := btrim(regexp_replace(coalesce(body,''), '\s+', ' ', 'g')); d date := (now() at time zone 'Asia/Jerusalem')::date; n int; why text;
begin
  if not exists (select 1 from passengers p where p.handle = hid) then raise exception 'not_a_passenger'; end if;
  if char_length(b) < 3 or char_length(b) > 200 then raise exception 'bad_length'; end if;
  select count(*) into n from ideas i where i.handle = hid and (i.created_at at time zone 'Asia/Jerusalem')::date = d;
  if n >= 3 then raise exception 'limit'; end if;
  why := mod_check(b);
  if why is not null then raise exception 'mod_%', why; end if;
  insert into ideas(handle, body) values (hid, b);
  return json_build_object('left', 2 - n);
end $$;
revoke all on function public.submit_idea(text, text) from public;
grant execute on function public.submit_idea(text, text) to anon, authenticated;

create or replace function public.ideas_left(h text) returns int
language sql stable security definer set search_path = public as $$
  select greatest(0, 3 - count(*))::int from ideas i where i.handle = lower(btrim(coalesce(h,''))) and (i.created_at at time zone 'Asia/Jerusalem')::date = (now() at time zone 'Asia/Jerusalem')::date
$$;
revoke all on function public.ideas_left(text) from public;
grant execute on function public.ideas_left(text) to anon, authenticated;

-- ================= 5. MISSIONS DU JOUR =================
create table if not exists public.mission_done (
  day     date not null,
  handle  text not null,
  mission text not null,
  bonus   int  not null,
  done_at timestamptz not null default now(),
  primary key (day, handle, mission)
);
alter table public.mission_done enable row level security;
revoke all on public.mission_done from anon, authenticated;

-- 3 missions par jour, tirées du jour (mêmes pour tous) : 1 facile + 1 pièces + 1 sociale
create or replace function public.missions_of(d date) returns table(id text, title text, goal int, bonus int)
language plpgsql immutable as $$
declare x bigint := abs(hashtext('tovim' || d::text)::bigint);
begin
  return query select * from (values
    ('login','🚢 עלו לסיפון היום',1,10),
    ('chat','💬 כתבו הודעה בצ''אט של הנוסעים',1,10),
    ('idea','💡 הציעו רעיון בתיבת הרעיונות',1,15)) a(id,title,goal,bonus) offset (x % 3) limit 1;
  return query select * from (values
    ('coins50','🪙 אספו 50 מטבעות על הסיפון',50,15),
    ('coins100','🪙 אספו 100 מטבעות על הסיפון',100,25),
    ('coins200','🪙 אספו 200 מטבעות על הסיפון',200,40)) b(id,title,goal,bonus) offset ((x / 3) % 3) limit 1;
  return query select * from (values
    ('comment','📸 הגיבו על הפוסט של היום באינסטגרם',1,30),
    ('invite','📣 הביאו חבר/ה חדש/ה לסיפון (הקישור האישי)',1,50)) c(id,title,goal,bonus) offset ((x / 9) % 2) limit 1;
end $$;

-- calcule la progression, valide (et crédite) ce qui est atteint ; "just" = validé à l'instant
create or replace function public.missions_sync(h text) returns json
language plpgsql security definer set search_path = public as $$
declare hid text := lower(btrim(coalesce(h,''))); d date := (now() at time zone 'Asia/Jerusalem')::date; m record; p int; done boolean; just boolean; out jsonb := '[]'::jsonb;
begin
  if not exists (select 1 from passengers x where x.handle = hid) then raise exception 'not_a_passenger'; end if;
  for m in select * from missions_of(d) loop
    p := case
      when m.id = 'login' then 1
      when m.id = 'chat' then (select count(*) from messages x where x.handle = hid and not x.hidden and (x.created_at at time zone 'Asia/Jerusalem')::date = d)
      when m.id = 'idea' then (select count(*) from ideas x where x.handle = hid and (x.created_at at time zone 'Asia/Jerusalem')::date = d)
      when m.id like 'coins%' then coalesce((select x.coins from coins_daily x where x.handle = hid and x.day = d), 0)
      when m.id = 'comment' then (select count(*) from billet_eligible x where x.handle = hid and x.day = d)
      when m.id = 'invite' then (select count(*) from passengers x where x.referred_by = hid and (x.created_at at time zone 'Asia/Jerusalem')::date = d)
      else 0 end;
    done := exists (select 1 from mission_done x where x.day = d and x.handle = hid and x.mission = m.id);
    just := false;
    if not done and p >= m.goal then
      insert into mission_done(day, handle, mission, bonus) values (d, hid, m.id, m.bonus) on conflict do nothing;
      if found then perform credit_coins(hid, m.bonus); just := true; end if;
      done := true;
    end if;
    out := out || jsonb_build_object('id', m.id, 'title', m.title, 'goal', m.goal, 'progress', least(p, m.goal), 'bonus', m.bonus, 'done', done, 'just', just);
  end loop;
  return json_build_object('day', d, 'missions', out, 'coins', coalesce((select x.coins from coins_daily x where x.handle = hid and x.day = d), 0));
end $$;
revoke all on function public.missions_sync(text) from public;
grant execute on function public.missions_sync(text) to anon, authenticated;

-- ================= 6. STATISTIQUES =================
-- abonnés Instagram : game_state 'ig' = {"followers": N}, mis à jour par la routine
create or replace function public.global_stats() returns json
language plpgsql stable security definer set search_path = public as $$
declare d date := (now() at time zone 'Asia/Jerusalem')::date; n bigint; caps int[] := ship_caps(); nxt int;
begin
  select count(*) into n from passengers;
  select c into nxt from unnest(caps) c where c > n order by c limit 1;
  return json_build_object(
    'passengers', n,
    'vip', (select count(*) from passengers where vip),
    'followers', (select (value->>'followers')::int from game_state where key = 'ig'),
    'left', greatest(0, coalesce(nxt, n) - n), 'next_cap', nxt,
    'sinks', (select count(*) from sinks),
    'coins_today', coalesce((select sum(coins) from coins_daily where day = d), 0),
    'players_today', (select count(*) from coins_daily where day = d and coins > 0),
    'wins', (select count(*) from treasure_wins));
end $$;
revoke all on function public.global_stats() from public;
grant execute on function public.global_stats() to anon, authenticated;

create or replace function public.my_stats(h text) returns json
language plpgsql stable security definer set search_path = public as $$
declare hid text := lower(btrim(coalesce(h,''))); d date := (now() at time zone 'Asia/Jerusalem')::date; p record; ct int; ca int;
begin
  select * into p from passengers x where x.handle = hid;
  if not found then return null; end if;
  ct := coalesce((select coins from coins_daily where handle = hid and day = d), 0);
  ca := coalesce((select total from coins where handle = hid), 0);
  return json_build_object(
    'coins_today', ct, 'coins_total', ca,
    'streak', p.streak, 'best_streak', p.best_streak, 'refs', p.refs, 'since', (p.created_at at time zone 'Asia/Jerusalem')::date,
    'missions', (select count(*) from mission_done where handle = hid),
    'missions_today', (select count(*) from mission_done where handle = hid and day = d),
    'participations', (select count(*) from coins_daily c join billet_eligible e on e.day = c.day and e.handle = c.handle where c.handle = hid and c.coins >= 200),
    'wins', (select count(*) from treasure_wins where handle = hid),
    'rank_today', case when ct > 0 then (select count(*) + 1 from coins_daily where day = d and coins > ct and handle <> 'tovim_beyachad') end,
    'rank_all', case when ca > 0 then (select count(*) + 1 from coins where total > ca and handle <> 'tovim_beyachad') end,
    'access', billet_access(hid), 'unlocked', billets_unlocked());
end $$;
revoke all on function public.my_stats(text) from public;
grant execute on function public.my_stats(text) to anon, authenticated;

-- ================= 7. CLASSEMENTS (jour / général) =================
create or replace function public.leaderboard(h text, scope text default 'today') returns json
language sql stable security definer set search_path = public as $$
  with d as (select (now() at time zone 'Asia/Jerusalem')::date as d),
  lb as (
    select handle, total as v from coins where scope = 'all' and total > 0 and handle <> 'tovim_beyachad'
    union all
    select c.handle, c.coins from coins_daily c, d where scope <> 'all' and c.day = d.d and c.coins > 0 and c.handle <> 'tovim_beyachad'),
  rk as (select handle, v as coins, rank() over (order by v desc)::int as rank from lb)
  select json_build_object('scope', scope,
    'top', coalesce((select json_agg(t order by t.rank, t.handle) from (select * from rk order by rank, handle limit 10) t), '[]'::json),
    'me', (select row_to_json(rk) from rk where rk.handle = lower(btrim(coalesce(h,'')))),
    'count', (select count(*) from rk))
$$;
revoke all on function public.leaderboard(text, text) from public;
grant execute on function public.leaderboard(text, text) to anon, authenticated;
