-- V7 (règlement du 03.11.2026) : PALIERS. Tous les 10 nouveaux passagers → +100 pièces pour TOUT le monde (comptent aussi
-- dans les pièces du jour = billet de loterie du jour) + actualité. Tous les 100 → grand événement (à faire par la routine).
-- Point de départ : 40 (passagers au 03.11 = 48) → prochain palier de 10 : 50 ; prochain palier de 100 : 100.
insert into public.game_state(key, value) values ('milestones', jsonb_build_object('last10', 40, 'last100', 0))
  on conflict (key) do nothing;

create or replace function public.check_milestones() returns json language plpgsql security definer set search_path to 'public' as $function$
declare n int; st jsonb; l10 int; l100 int; tens int[] := '{}'; hundreds int[] := '{}'; k int; h text;
begin
  select count(*) into n from passengers;
  select value into st from game_state where key = 'milestones' for update;
  l10 := coalesce((st->>'last10')::int, (n/10)*10); l100 := coalesce((st->>'last100')::int, (n/100)*100);
  k := l10 + 10;
  while k <= n loop
    tens := tens || k;
    for h in select handle from passengers where handle <> all(lottery_excluded()) loop perform credit_coins(h, 100); end loop;
    insert into news(title, body) values ('🎉 ' || k || ' נוסעים על הסיפון!', 'כל הנוסעים קיבלו מתנה: 🪙 100 מטבעות (זה גם כרטיס להגרלה של היום – רק להגיב על הפוסט של היום 💬)
כל 10 נוסעים חדשים = עוד מתנה לכולם. כל 100 = אירוע ענק בספינה 🌊');
    k := k + 10;
  end loop;
  k := l100 + 100;
  while k <= n loop hundreds := hundreds || k; k := k + 100; end loop;
  update game_state set value = jsonb_build_object('last10', greatest(l10, (n/10)*10), 'last100', greatest(l100, (n/100)*100)), updated_at = now() where key = 'milestones';
  return json_build_object('passengers', n, 'ten', to_json(tens), 'hundred', to_json(hundreds), 'next10', (greatest(l10,(n/10)*10)) + 10);
end $function$;
revoke all on function public.check_milestones() from public, anon, authenticated;
