-- 1.11.2026 : correctif. L'ajout groupé de 11 abonnés le 30.10 (23 -> 34 d'un coup) a sauté le palier 25 : le trigger
-- ne testait que « n = cap ». Naufrage n°1 enregistré à la main le 1.11 (ship_idx 0, 25e passager __yarin__10).
-- Désormais : naufrage dès que n >= cap et qu'il n'existe pas encore.
create or replace function public.after_passenger_insert() returns trigger
language plpgsql security definer set search_path = public as $$
declare n bigint; caps int[] := ship_caps(); i int;
begin
  select count(*) into n from passengers;
  for i in 1..array_length(caps,1) loop
    if n >= caps[i] and not exists (select 1 from sinks where ship_idx = i - 1) then
      insert into sinks(ship_idx, handle) values (i - 1, new.handle) on conflict do nothing;
    end if;
  end loop;
  return null;
end $$;
