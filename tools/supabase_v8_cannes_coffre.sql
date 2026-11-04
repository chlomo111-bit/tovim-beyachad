-- V8 (04.11.2026, Shlomo : « applique tout ») — tout est virtuel, aucun vrai argent.
-- 1) Boutique de cannes à pêche (idée de @amit_azulay23) : plus la canne est chère, plus les gros poissons arrivent.
-- 2) Bonus de série : 3 jours d'affilée = 150 pièces, 7 jours = 500 pièces + chapeau de capitaine.
-- 3) Coffre du jour caché sur le pont : 200 pièces, une fois par jour.
-- 4) Classement des recruteurs de la semaine + prix (500 pièces + chapeau de capitaine).

-- ---------- 1) CANNES ----------
create table if not exists public.rods_owned (handle text not null, rod text not null, bought_at timestamptz not null default now(), primary key (handle, rod));
create table if not exists public.rod_state (handle text primary key, rod text not null default 'wood');
alter table public.rods_owned enable row level security;
alter table public.rod_state enable row level security;

create or replace function public.rod_price(rod text) returns int language sql immutable as $$
  select case rod when 'pro' then 300 when 'carbon' then 800 when 'legend' then 1500 else null end $$;
-- facteur de chance : r = 1 - (1-random())*k  → moins de chaussures/sardines, plus de thons/requins
create or replace function public.rod_k(rod text) returns float language sql immutable as $$
  select case rod when 'pro' then .88 when 'carbon' then .76 when 'legend' then .64 else 1.0 end $$;

create or replace function public.my_rods(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @'));
begin
  return json_build_object('rod', coalesce((select rod from rod_state where handle = hh), 'wood'),
    'owned', coalesce((select json_agg(rod) from rods_owned where handle = hh), '[]'::json),
    'coins', coalesce((select total from coins where handle = hh), 0));
end $function$;
grant execute on function public.my_rods(text) to anon, authenticated;

create or replace function public.buy_rod(h text, rod text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); pr int := rod_price(rod); tot int;
begin
  if pr is null then return json_build_object('error','not_for_sale'); end if;
  if not exists (select 1 from passengers where handle = hh) then return json_build_object('error','not_passenger'); end if;
  if exists (select 1 from rods_owned where handle = hh and rods_owned.rod = buy_rod.rod) then return json_build_object('error','owned'); end if;
  select total into tot from coins where handle = hh for update;
  if coalesce(tot,0) < pr then return json_build_object('error','not_enough','coins',coalesce(tot,0),'price',pr); end if;
  update coins set total = total - pr where handle = hh;
  insert into rods_owned(handle, rod) values (hh, rod);
  insert into rod_state(handle, rod) values (hh, rod) on conflict (handle) do update set rod = excluded.rod;
  return json_build_object('ok', true, 'rod', rod, 'coins', tot - pr);
end $function$;
grant execute on function public.buy_rod(text, text) to anon, authenticated;

create or replace function public.use_rod(h text, rod text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @'));
begin
  if rod <> 'wood' and not exists (select 1 from rods_owned where handle = hh and rods_owned.rod = use_rod.rod) then return json_build_object('error','not_owned'); end if;
  insert into rod_state(handle, rod) values (hh, rod) on conflict (handle) do update set rod = excluded.rod;
  return json_build_object('ok', true, 'rod', rod);
end $function$;
grant execute on function public.use_rod(text, text) to anon, authenticated;

create or replace function public.catch_fish(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); d date := (now() at time zone 'Asia/Jerusalem')::date;
  last timestamptz; n int; rd text; r float; sp text; em text; g int; c int; best int; rk int;
begin
  if not exists (select 1 from passengers where handle = hh) then return json_build_object('error','not_passenger'); end if;
  select max(caught_at) into last from fish_catches where handle = hh;
  if last is not null and now() - last < interval '10 seconds' then
    return json_build_object('error','wait','wait', ceil(10 - extract(epoch from now() - last))); end if;
  select count(*) into n from fish_catches where handle = hh and (caught_at at time zone 'Asia/Jerusalem')::date = d;
  if n >= 40 then return json_build_object('error','limit','left',0); end if;
  rd := coalesce((select rod from rod_state where handle = hh), 'wood');
  r := 1 - (1 - random()) * rod_k(rd);
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
  return json_build_object('species', sp, 'emoji', em, 'grams', g, 'coins', c, 'best', best, 'rank', rk, 'left', 40 - n - 1, 'rod', rd);
end $function$;
grant execute on function public.catch_fish(text) to anon, authenticated;

-- ---------- 2) BONUS DE SÉRIE ----------
create table if not exists public.streak_rewards (handle text not null, milestone int not null, day date not null, primary key (handle, milestone, day));
alter table public.streak_rewards enable row level security;

create or replace function public.streak_bonus(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); d date := (now() at time zone 'Asia/Jerusalem')::date; s int; m int; amt int;
begin
  select streak into s from passengers where handle = hh;
  if s is null then return json_build_object('error','not_passenger'); end if;
  if s >= 7 then m := 7; elsif s >= 3 then m := 3; else return json_build_object('streak', s, 'bonus', 0); end if;
  -- une seule récompense par palier et par série (pas déjà reçue depuis le début de cette série)
  if exists (select 1 from streak_rewards where handle = hh and milestone = m and day > d - s) then return json_build_object('streak', s, 'bonus', 0); end if;
  amt := case m when 7 then 500 else 150 end;
  insert into streak_rewards(handle, milestone, day) values (hh, m, d);
  perform credit_coins(hh, amt);
  if m = 7 then insert into hats_owned(handle, hat) values (hh, 'captain') on conflict do nothing; end if;
  return json_build_object('streak', s, 'bonus', amt, 'milestone', m);
end $function$;
grant execute on function public.streak_bonus(text) to anon, authenticated;

-- ---------- 3) COFFRE DU JOUR ----------
create table if not exists public.chest_claims (handle text not null, day date not null, claimed_at timestamptz not null default now(), primary key (handle, day));
alter table public.chest_claims enable row level security;

create or replace function public.claim_chest(h text) returns json language plpgsql security definer set search_path to 'public' as $function$
declare hh text := lower(btrim(coalesce(h,''),' @')); d date := (now() at time zone 'Asia/Jerusalem')::date; n int;
begin
  if not exists (select 1 from passengers where handle = hh) then return json_build_object('error','not_passenger'); end if;
  if exists (select 1 from chest_claims where handle = hh and day = d) then return json_build_object('error','already'); end if;
  insert into chest_claims(handle, day) values (hh, d);
  perform credit_coins(hh, 200);
  select count(*) into n from chest_claims where day = d;
  return json_build_object('ok', true, 'coins', 200, 'rank', n);
end $function$;
grant execute on function public.claim_chest(text) to anon, authenticated;

-- ---------- 4) RECRUTEURS DE LA SEMAINE ----------
create or replace function public.recruit_board() returns json language sql security definer set search_path to 'public' as $$
  select coalesce(json_agg(t), '[]'::json) from (
    select referred_by as handle, count(*) as n from passengers
    where referred_by is not null and (created_at at time zone 'Asia/Jerusalem')::date >= il_week()
    group by referred_by order by count(*) desc, min(created_at) limit 5) t $$;
grant execute on function public.recruit_board() to anon, authenticated;

create table if not exists public.recruit_awards (week date primary key, handle text, n int, awarded_at timestamptz default now());
alter table public.recruit_awards enable row level security;

-- samedi soir (après Shabbat) : 500 pièces + chapeau de capitaine au meilleur recruteur de la semaine
create or replace function public.award_recruiter_week() returns json language plpgsql security definer set search_path to 'public' as $function$
declare w date := il_week(); hh text; k int;
begin
  if exists (select 1 from recruit_awards where week = w) then return (select row_to_json(a) from recruit_awards a where week = w); end if;
  select referred_by, count(*) into hh, k from passengers
    where referred_by is not null and (created_at at time zone 'Asia/Jerusalem')::date >= w
    group by referred_by order by count(*) desc, min(created_at) limit 1;
  insert into recruit_awards(week, handle, n) values (w, hh, k);
  if hh is not null then perform credit_coins(hh, 500); insert into hats_owned(handle, hat) values (hh, 'captain') on conflict do nothing; end if;
  return json_build_object('week', w, 'handle', hh, 'n', k);
end $function$;
revoke all on function public.award_recruiter_week() from public, anon, authenticated;
