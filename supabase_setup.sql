-- FCWB Materialbestellung – Datenbank
-- Im Supabase SQL Editor einfügen und ausführen. Mehrfach ausführbar.
--
-- WICHTIG, falls die Adresse des Vereinskontos einmal ändert: sie steht weiter unten
-- in beiden Policies und muss dort angepasst werden (zweimal ersetzen), sonst kommt
-- niemand mehr an die Daten.

-- Eine Zeile pro Bestellung / pro Team, damit gleichzeitige Änderungen
-- verschiedener Personen sich nicht gegenseitig überschreiben.
create table if not exists public.orders (
  id         text primary key,
  data       jsonb not null,
  pos        bigint not null default (extract(epoch from now())*1000)::bigint,
  updated_at timestamptz not null default now()
);
create table if not exists public.teams (
  id         text primary key,
  data       jsonb not null,
  pos        bigint not null default (extract(epoch from now())*1000)::bigint,
  updated_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Zugriff nur für das angemeldete Vereinskonto.
--
-- Der Schlüssel, der in der Seite steht (sb_publishable_…), ist öffentlich – er steht
-- im HTML und in der Git-Historie und lässt sich nicht zurückholen. Er allein darf
-- deshalb nichts können: Die Rolle "anon" bekommt keine Policy, Lesen liefert damit
-- eine leere Liste und Schreiben wird abgewiesen.
--
-- Die Prüfung hängt zusätzlich an der Mailadresse des Vereinskontos, nicht nur an
-- "irgendwie angemeldet". Damit bleiben die Daten auch dann geschützt, wenn in Supabase
-- versehentlich die freie Registrierung aktiv ist: Ein selbst angelegtes Konto wäre zwar
-- "authenticated", käme hier aber trotzdem nicht durch.
-- ---------------------------------------------------------------------------
alter table public.orders enable row level security;
alter table public.teams  enable row level security;

-- alte, offene Policies aus der ersten Version entfernen
drop policy if exists "orders_all" on public.orders;
drop policy if exists "teams_all"  on public.teams;
drop policy if exists "orders_auth" on public.orders;
drop policy if exists "teams_auth"  on public.teams;

create policy "orders_auth" on public.orders for all to authenticated
  using      ((auth.jwt() ->> 'email') = 'bestellung@fcwb-shop.ch')
  with check ((auth.jwt() ->> 'email') = 'bestellung@fcwb-shop.ch');

create policy "teams_auth" on public.teams for all to authenticated
  using      ((auth.jwt() ->> 'email') = 'bestellung@fcwb-shop.ch')
  with check ((auth.jwt() ->> 'email') = 'bestellung@fcwb-shop.ch');

-- Live-Sync (prüft dieselben Policies).
-- "add table" bricht mit Fehler ab, wenn die Tabelle schon in der Publikation ist –
-- und weil der SQL-Editor alles in einer Transaktion ausführt, wäre damit auch die
-- Absicherung oben wieder verworfen. Deshalb vorher nachsehen.
do $$
begin
  if not exists (select 1 from pg_publication_tables
                 where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'orders') then
    alter publication supabase_realtime add table public.orders;
  end if;
  if not exists (select 1 from pg_publication_tables
                 where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'teams') then
    alter publication supabase_realtime add table public.teams;
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Weckruf-Tabelle (seit 06.10.2026).
--
-- Supabase pausiert Free-Projekte nach 7 Tagen ohne «ausreichende» Aktivität.
-- Der GitHub-Wecker fragte bisher `orders` ab. Seit der Absicherung bekommt der
-- öffentliche Schlüssel dort eine leere Liste zurück – und eine Anfrage, die nichts
-- liefert, zählte offenbar nicht als Nutzung (Warnmail von Supabase am 05.10.2026).
--
-- Diese Tabelle hat genau eine Zeile, die jeder lesen darf. Sie enthält nichts ausser
-- einem Zeitstempel und ist absichtlich uninteressant. Geschrieben wird sie nie – es
-- gibt keine Schreib-Policy, auch nicht fuer das Vereinskonto. Sie existiert nur,
-- damit der Weckruf eine echte Antwort bekommt statt einer leeren Liste.
-- ---------------------------------------------------------------------------
create table if not exists public.heartbeat (
  id   int primary key,
  ping timestamptz not null default now(),
  constraint heartbeat_nur_eine_zeile check (id = 1)
);
insert into public.heartbeat (id) values (1) on conflict (id) do nothing;

alter table public.heartbeat enable row level security;
drop policy if exists "heartbeat_read" on public.heartbeat;
create policy "heartbeat_read" on public.heartbeat for select to anon, authenticated using (true);

-- ---------------------------------------------------------------------------
-- Kontrolle nach dem Ausführen: beide Zeilen müssen rowsecurity = true zeigen,
-- und es dürfen nur die beiden Policies oben auftauchen, keine mit "anon" oder "public".
-- ---------------------------------------------------------------------------
-- select tablename, rowsecurity from pg_tables
--   where schemaname='public' and tablename in ('orders','teams');
-- select tablename, policyname, roles, cmd from pg_policies
--   where schemaname='public' order by tablename, policyname;
--
-- Bewusst OHNE Einschraenkung auf bestimmte Tabellen. Genau diese Einschraenkung hat
-- am 23.09.2026 die offene Tabelle `meta` verdeckt: Sie stand nicht in der Liste und
-- tauchte deshalb im Ergebnis nicht auf. Es darf keine Policy fuer `public` oder
-- `anon` geben ausser `heartbeat_read`.

-- ---------------------------------------------------------------------------
-- Alte Tabelle `meta` aus der ersten Supabase-Fassung: je eine Zeile für `orders`
-- und `teams` mit der kompletten Liste als JSON. Die App benutzt sie nicht mehr,
-- sie enthält aber weiterhin den Stand vom 09.09.2026 – also echte Bestelldaten
-- mit Spielernamen.
--
-- Bis zum 06.10.2026 stand sie offen: Policies `meta_read` und `meta_write` für die
-- Rolle `public`, lesbar UND änderbar allein mit dem öffentlichen Schlüssel. Die
-- Absicherung vom 23.09.2026 hatte nur `orders` und `teams` erfasst, weil die
-- Kontrollabfrage auf diese beiden Namen eingeschränkt war.
--
-- Sie bekommt hier dieselbe Prüfung wie die anderen Tabellen. Falls der alte Stand
-- nicht mehr gebraucht wird, kann die Tabelle später ersatzlos weg – das ist eine
-- eigene Entscheidung und nicht Teil dieser Datei.
-- ---------------------------------------------------------------------------
do $$
begin
  if to_regclass('public.meta') is not null then
    execute 'alter table public.meta enable row level security';
    execute 'drop policy if exists "meta_read"  on public.meta';
    execute 'drop policy if exists "meta_write" on public.meta';
    execute 'drop policy if exists "meta_auth"  on public.meta';
    execute 'create policy "meta_auth" on public.meta for all to authenticated
               using      ((auth.jwt() ->> ''email'') = ''bestellung@fcwb-shop.ch'')
               with check ((auth.jwt() ->> ''email'') = ''bestellung@fcwb-shop.ch'')';
  end if;
end $$;
