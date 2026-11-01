-- V6 (1.11.2026, validé par Shlomo) : seuil de la loterie 100 pièces, PÊCHE (idée de @shahar_b.y) et BOUTIQUE DE CHAPEAUX (idée de @mor.levi134).

-- ===== Seuil 100 pièces =====
create or replace function public.lottery_eligible(d date) returns table(handle text) language sql stable security definer set search_path to 'public' as $f$
  select c.handle from coins_daily c
  where c.day = d and c.coins >= 100 and c.handle <> all(lottery_excluded())
    and exists (select 1 from billet_eligible b where b.day = d and b.handle = c.handle)
$f$;
revoke all on function public.lottery_eligible(date) from public, anon, authenticated;

-- meilleur commentateur d'un jour : commentaires valables, textes identiques comptés une seule fois,
-- égalité = celui qui a atteint ce nombre en premier
create or replace function public.top_commenter_of(d date) returns table(handle text, n int, reached_at timestamptz)
language sql stable security definer set search_path to 'public' as $f$
  with x as (
    select distinct on (l.handle, lower(btrim(coalesce(l.body,'')))) l.handle, l.commented_at
    from ig_comment_log l
    where l.valid and (l.commented_at at time zone 'Asia/Jerusalem')::date = d and l.handle <> all(lottery_excluded())
    order by l.handle, lower(btrim(coalesce(l.body,''))), l.commented_at),
  v as (select x.handle, x.commented_at, row_number() over (partition by x.handle order by x.commented_at) rn from x),
  c as (select v.handle, max(v.rn) n from v group by v.handle)
  select c.handle, c.n::int, v.commented_at from c join v on v.handle = c.handle and v.rn = c.n
  order by c.n desc, v.commented_at asc limit 1
$f$;
revoke all on function public.top_commenter_of(date) from public, anon, authenticated;

create or replace function public.run_lottery(d date) returns json language plpgsql security definer set search_path to 'public' as $function$
declare w text; n int; r record; t record;
begin
  select * into r from lottery_draws where day = d;
  if found then return json_build_object('already', true, 'day', d, 'winner', r.winner, 'entrants', r.entrants, 'top', r.top_commenter, 'top_n', r.top_count); end if;
  if now() < lottery_draw_at(d) then return json_build_object('error', 'too_early', 'draw_at', lottery_draw_at(d)); end if;
  select count(*) into n from lottery_eligible(d);
  select e.handle into w from lottery_eligible(d) e order by random() limit 1;
  select * into t from top_commenter_of(d);
  insert into lottery_draws(day, winner, entrants, top_commenter, top_count, top_wish_status)
    values (d, w, n, t.handle, t.n, case when t.handle is null then 'none' else 'pending' end)
    on conflict (day) do nothing;
  select * into r from lottery_draws where day = d;
  return json_build_object('day', d, 'winner', r.winner, 'entrants', r.entrants, 'top', r.top_commenter, 'top_n', r.top_count);
end $function$;

create or replace function public.lottery_state(h text default '') returns json language plpgsql security definer set search_path to 'public' as $function$
declare d date := (now() at time zone 'Asia/Jerusalem')::date; hh text := lower(btrim(coalesce(h,''),' @')); my int; com boolean; n int;
  nxt date; lw record; t record; crown record; dow int := extract(isodow from (now() at time zone 'Asia/Jerusalem'));
  shab boolean;
begin
  select coalesce(c.coins,0) into my from coins_daily c where c.handle = hh and c.day = d;
  com := exists(select 1 from billet_eligible b where b.day = d and b.handle = hh);
  select count(*) into n from lottery_eligible(d);
  -- prochain tirage non fait (le samedi avant 20:00 : celui du vendredi)
  select k::date into nxt from generate_series(d - 1, d, interval '1 day') k
    where k::date >= date '2026-10-30' and not exists (select 1 from lottery_draws l where l.day = k::date) order by k limit 1;
  select * into lw from lottery_draws l where l.winner is not null order by l.day desc limit 1;
  select * into crown from lottery_draws l where l.top_commenter is not null order by l.day desc limit 1;
  select * into t from top_commenter_of(d);
  shab := (dow = 5 and (now() at time zone 'Asia/Jerusalem')::time >= time '16:00') or (dow = 6 and (now() at time zone 'Asia/Jerusalem')::time < time '18:30');
  return json_build_object('day', d, 'threshold', 100, 'mine', coalesce(my,0), 'commented', com,
    'entered', coalesce(my,0) >= 100 and com, 'entrants', n,
    'draw_at', lottery_draw_at(d), 'next_day', nxt, 'next_at', case when nxt is null then null else lottery_draw_at(nxt) end,
    'friday', dow = 5, 'shabbat', shab,
    'drawn_today', exists(select 1 from lottery_draws l where l.day = d),
    'last_winner', lw.winner, 'last_day', lw.day, 'last_entrants', lw.entrants,
    'crown', crown.top_commenter, 'crown_day', crown.day, 'crown_n', crown.top_count,
    'top_now', t.handle, 'top_now_n', t.n, 'now', now());
end $function$;

-- ===== PÊCHE =====
create table if not exists public.fish_catches (
  id bigserial primary key, handle text not null, species text not null, emoji text not null,
  grams int not null, coins int not null, week date not null, caught_at timestamptz not null default now());
create index if not exists fish_week_idx on public.fish_catches(week, grams desc);
create index if not exists fish_handle_idx on public.fish_catches(handle, caught_at desc);
alter table public.fish_catches enable row level security;
create table if not exists public.fish_awards (week date primary key, first text, second text, third text, awarded_at timestamptz default now());
alter table public.fish_awards enable row level security;

-- semaine de dimanche à samedi (heure d'Israël)
create or replace function public.il_week(ts timestamptz default now()) returns date language sql stable as $$
  select ((ts at time zone 'Asia/Jerusalem')::date - extract(dow from (ts at time zone 'Asia/Jerusalem'))::int) $$;

create or replace function public.catch_fish(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); d date := (now() at time zone 'Asia/Jerusalem')::date;
  last timestamptz; n int; r float := random(); sp text; em text; g int; c int; best int; rk int;
begin
  if not exists (select 1 from passengers where handle = hh) then return json_build_object('error','not_passenger'); end if;
  select max(caught_at) into last from fish_catches where handle = hh;
  if last is not null and now() - last < interval '10 seconds' then
    return json_build_object('error','wait','wait', ceil(10 - extract(epoch from now() - last))); end if;
  select count(*) into n from fish_catches where handle = hh and (caught_at at time zone 'Asia/Jerusalem')::date = d;
  if n >= 40 then return json_build_object('error','limit','left',0); end if;
  if r < .08 then sp := 'נעל ישנה'; em := '👢'; g := 0;
  elsif r < .52 then sp := 'סרדין'; em := '🐟'; g := 80 + floor(random()*320);
  elsif r < .78 then sp := 'דניס'; em := '🐠'; g := 400 + floor(random()*1100);
  elsif r < .92 then sp := 'לוקוס'; em := '🐡'; g := 1500 + floor(random()*3500);
  elsif r < .985 then sp := 'טונה'; em := '🐟'; g := 5000 + floor(random()*20000);
  else sp := 'כריש תינוק'; em := '🦈'; g := 25000 + floor(random()*35000); end if;
  c := greatest(1, round(g / 200.0));
  insert into fish_catches(handle, species, emoji, grams, coins, week) values (hh, sp, em, g, c, il_week());
  perform credit_coins(hh, c);
  select max(grams) into best from fish_catches where handle = hh and week = il_week();
  select count(*) + 1 into rk from (select handle, max(grams) m from fish_catches where week = il_week() group by handle) t where t.m > best;
  return json_build_object('species', sp, 'emoji', em, 'grams', g, 'coins', c, 'best', best, 'rank', rk, 'left', 40 - n - 1);
end $function$;
grant execute on function public.catch_fish(text) to anon, authenticated;

create or replace function public.fish_board(h text default '') returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); w date := il_week(); d date := (now() at time zone 'Asia/Jerusalem')::date;
  top json; mybest int; myrank int; n int; lastw json;
begin
  select coalesce(json_agg(t), '[]'::json) into top from (
    select handle, grams, species, emoji from (
      select distinct on (handle) handle, grams, species, emoji from fish_catches where week = w order by handle, grams desc) x
    order by grams desc limit 10) t;
  select max(grams) into mybest from fish_catches where handle = hh and week = w;
  if mybest is not null then
    select count(*) + 1 into myrank from (select handle, max(grams) m from fish_catches where week = w group by handle) t where t.m > mybest; end if;
  select count(*) into n from fish_catches where handle = hh and (caught_at at time zone 'Asia/Jerusalem')::date = d;
  select row_to_json(a) into lastw from fish_awards a order by week desc limit 1;
  return json_build_object('week', w, 'top', top, 'mybest', mybest, 'myrank', myrank, 'left', greatest(0, 40 - n), 'last', lastw);
end $function$;
grant execute on function public.fish_board(text) to anon, authenticated;

-- prix de la semaine (appelé par la routine samedi soir) : 1 000 / 500 / 250 pièces + chapeau « trophy » au 1er
create or replace function public.award_fishing_week(w date) returns json language plpgsql security definer set search_path to 'public' as $function$
declare t text[];
begin
  if exists (select 1 from fish_awards where week = w) then return (select row_to_json(a) from fish_awards a where week = w); end if;
  select array_agg(handle order by m desc) into t from (select handle, max(grams) m from fish_catches where week = w group by handle order by m desc limit 3) s;
  insert into fish_awards(week, first, second, third) values (w, t[1], t[2], t[3]);
  if t[1] is not null then perform credit_coins(t[1], 1000); insert into hats_owned(handle, hat) values (t[1], 'trophy') on conflict do nothing; end if;
  if t[2] is not null then perform credit_coins(t[2], 500); end if;
  if t[3] is not null then perform credit_coins(t[3], 250); end if;
  return (select row_to_json(a) from fish_awards a where week = w);
end $function$;
revoke all on function public.award_fishing_week(date) from public, anon, authenticated;

-- ===== BOUTIQUE DE CHAPEAUX =====
create table if not exists public.hats_owned (handle text not null, hat text not null, bought_at timestamptz not null default now(), primary key (handle, hat));
alter table public.hats_owned enable row level security;

create or replace function public.hat_price(hat text) returns int language sql immutable as $$
  select case hat when 'cap' then 100 when 'beanie' then 150 when 'straw' then 200 when 'bucket' then 250
    when 'chef' then 350 when 'party' then 350 when 'pirate' then 500 when 'tophat' then 700 else null end $$;

create or replace function public.my_hats(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @'));
begin
  return json_build_object('owned', coalesce((select json_agg(hat) from hats_owned where handle = hh), '[]'::json),
    'wearing', (select style->>'hat' from passengers where handle = hh),
    'coins', coalesce((select total from coins where handle = hh), 0));
end $function$;
grant execute on function public.my_hats(text) to anon, authenticated;

create or replace function public.buy_hat(h text, hat text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); pr int := hat_price(hat); tot int;
begin
  if pr is null then return json_build_object('error','not_for_sale'); end if;
  if not exists (select 1 from passengers where handle = hh) then return json_build_object('error','not_passenger'); end if;
  if exists (select 1 from hats_owned where handle = hh and hats_owned.hat = buy_hat.hat) then return json_build_object('error','owned'); end if;
  select total into tot from coins where handle = hh for update;
  if coalesce(tot,0) < pr then return json_build_object('error','not_enough','coins',coalesce(tot,0),'price',pr); end if;
  update coins set total = total - pr where handle = hh;
  insert into hats_owned(handle, hat) values (hh, hat);
  update passengers set style = coalesce(style,'{}'::jsonb) || jsonb_build_object('hat', hat) where handle = hh;
  return json_build_object('ok', true, 'hat', hat, 'coins', tot - pr);
end $function$;
grant execute on function public.buy_hat(text, text) to anon, authenticated;

create or replace function public.wear_hat(h text, hat text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @'));
begin
  if hat <> 'none' and not exists (select 1 from hats_owned where handle = hh and hats_owned.hat = wear_hat.hat) then return json_build_object('error','not_owned'); end if;
  update passengers set style = coalesce(style,'{}'::jsonb) || jsonb_build_object('hat', hat) where handle = hh;
  return json_build_object('ok', true, 'hat', hat);
end $function$;
grant execute on function public.wear_hat(text, text) to anon, authenticated;
