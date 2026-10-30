-- V4 (30.10.2026) : règles obligatoires de Shlomo pour tous les jeux.
-- La loterie quotidienne de 20 ₪ à 20:00 REMPLACE le billet caché (qui n'apparaissait qu'après le naufrage).
-- Conditions : (a) avoir commenté le POST DU JOUR (table billet_eligible, remplie par les passages)
--              (b) avoir récolté au moins 200 pièces dans la journée (coins_daily).
-- Shabbat : rien entre vendredi 16:00 et samedi 18:30 → le tirage du vendredi a lieu samedi à 20:00,
--           juste AVANT celui du samedi (vendredi d'abord). Le passage de samedi 19:55 enregistre les
--           commentateurs du post du vendredi.
-- Prix « המגיב של היום » : calculé au même moment, depuis ig_comment_log (rempli à chaque passage).

create table if not exists public.lottery_draws (
  day date primary key,
  winner text,
  entrants int not null default 0,
  top_commenter text,
  top_count int,
  top_wish text,                 -- ce que le meilleur commentateur a choisi pour le lendemain
  top_wish_status text,          -- pending | done | refused | none
  drawn_at timestamptz not null default now()
);
alter table public.lottery_draws enable row level security;
revoke all on public.lottery_draws from anon, authenticated;

-- journal de TOUS les commentaires Instagram des joueurs (pour « המגיב של היום »)
create table if not exists public.ig_comment_log (
  comment_id text primary key,
  handle text not null,
  media_id text,
  body text,
  commented_at timestamptz not null,
  valid boolean not null default true
);
create index if not exists ig_comment_log_day on public.ig_comment_log ((commented_at at time zone 'Asia/Jerusalem'));
alter table public.ig_comment_log enable row level security;
revoke all on public.ig_comment_log from anon, authenticated;

-- comptes de Shlomo / du jeu : jamais gagnants
create or replace function public.lottery_excluded() returns text[] language sql immutable as $f$
  select array['tovim_beyachad','chlomo.assouline','chlomo_assouline','the_noise_2026','hakaveret_shelanu','hasavta.shelanu']
$f$;

-- heure du tirage d'un jour : 20:00, sauf vendredi → samedi 20:00 (Shabbat)
create or replace function public.lottery_draw_at(d date) returns timestamptz language sql immutable as $f$
  select case when extract(isodow from d) = 5
    then (((d + 1)::text || ' 20:00')::timestamp at time zone 'Asia/Jerusalem')
    else ((d::text || ' 20:00')::timestamp at time zone 'Asia/Jerusalem') end
$f$;

create or replace function public.lottery_eligible(d date) returns table(handle text) language sql stable security definer set search_path to 'public' as $f$
  select c.handle from coins_daily c
  where c.day = d and c.coins >= 200 and c.handle <> all(lottery_excluded())
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
revoke all on function public.run_lottery(date) from public, anon, authenticated;

-- appelé par le jeu : fait les tirages dus (vendredi d'abord le samedi soir), renvoie le dernier résultat
create or replace function public.lottery_live() returns json language plpgsql security definer set search_path to 'public' as $function$
declare d date := (now() at time zone 'Asia/Jerusalem')::date; k date; res json := '[]'::json; r record;
begin
  for k in select g::date from generate_series(d - 2, d, interval '1 day') g order by 1 loop
    if k >= date '2026-10-30' and now() >= lottery_draw_at(k) and not exists (select 1 from lottery_draws where day = k) then
      perform run_lottery(k);
    end if;
  end loop;
  select coalesce(json_agg(json_build_object('day', l.day, 'winner', l.winner, 'entrants', l.entrants, 'top', l.top_commenter, 'top_n', l.top_count, 'drawn_at', l.drawn_at) order by l.day), '[]'::json)
    into res from lottery_draws l where l.drawn_at > now() - interval '3 hours';
  return json_build_object('recent', res, 'now', now());
end $function$;
grant execute on function public.lottery_live() to anon, authenticated;

-- état pour un joueur (pilule, fiche « היום שלי », couronne)
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
  return json_build_object('day', d, 'threshold', 200, 'mine', coalesce(my,0), 'commented', com,
    'entered', coalesce(my,0) >= 200 and com, 'entrants', n,
    'draw_at', lottery_draw_at(d), 'next_day', nxt, 'next_at', case when nxt is null then null else lottery_draw_at(nxt) end,
    'friday', dow = 5, 'shabbat', shab,
    'drawn_today', exists(select 1 from lottery_draws l where l.day = d),
    'last_winner', lw.winner, 'last_day', lw.day, 'last_entrants', lw.entrants,
    'crown', crown.top_commenter, 'crown_day', crown.day, 'crown_n', crown.top_count,
    'top_now', t.handle, 'top_now_n', t.n, 'now', now());
end $function$;
grant execute on function public.lottery_state(text) to anon, authenticated;

-- le billet caché est supprimé : plus aucun créneau ne s'ouvre
create or replace function public.billets_unlocked() returns boolean language sql stable security definer set search_path to 'public' as $f$ select false $f$;
