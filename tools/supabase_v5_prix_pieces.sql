-- V5 (31.10.2026, décision de Shlomo) : plus d'argent réel à partir du 1.11.2026.
-- Le gagnant de la loterie reçoit 1 000 pièces dans le jeu + le pouvoir de décider d'un événement extraordinaire le lendemain.
-- APPLIQUÉ en ligne le 01/11/2026 20:05 (la fonction run_lottery n'était pas à jour : prix du 1/11 crédité à la main à @shahar_b.y).
alter table public.lottery_draws add column if not exists prize_coins int not null default 0;
alter table public.lottery_draws add column if not exists winner_wish text;
alter table public.lottery_draws add column if not exists winner_wish_status text not null default 'none';

create or replace function public.run_lottery(d date) returns json language plpgsql security definer set search_path to 'public' as $function$
declare w text; n int; r record; t record; prize int := case when d >= date '2026-11-01' then 1000 else 0 end;
begin
  select * into r from lottery_draws where day = d;
  if found then return json_build_object('already', true, 'day', d, 'winner', r.winner, 'entrants', r.entrants, 'top', r.top_commenter, 'top_n', r.top_count, 'prize_coins', r.prize_coins); end if;
  if now() < lottery_draw_at(d) then return json_build_object('error', 'too_early', 'draw_at', lottery_draw_at(d)); end if;
  select count(*) into n from lottery_eligible(d);
  select e.handle into w from lottery_eligible(d) e order by random() limit 1;
  select * into t from top_commenter_of(d);
  insert into lottery_draws(day, winner, entrants, top_commenter, top_count, top_wish_status, prize_coins, winner_wish_status)
    values (d, w, n, t.handle, t.n, case when t.handle is null then 'none' else 'pending' end,
            case when w is null then 0 else prize end, case when w is null or prize = 0 then 'none' else 'pending' end)
    on conflict (day) do nothing;
  if w is not null and prize > 0 then
    insert into coins(handle, total, today, day, last_at) values (w, 0, 0, (now() at time zone 'Asia/Jerusalem')::date, now() - interval '1 minute') on conflict (handle) do nothing;
    update coins set total = total + prize where handle = w;
  end if;
  select * into r from lottery_draws where day = d;
  return json_build_object('day', d, 'winner', r.winner, 'entrants', r.entrants, 'top', r.top_commenter, 'top_n', r.top_count, 'prize_coins', r.prize_coins);
end $function$;
revoke all on function public.run_lottery(date) from public, anon, authenticated;
