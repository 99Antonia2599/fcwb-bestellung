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

-- Live-Sync (prüft dieselben Policies)
alter publication supabase_realtime add table public.orders;
alter publication supabase_realtime add table public.teams;

-- ---------------------------------------------------------------------------
-- Kontrolle nach dem Ausführen: beide Zeilen müssen rowsecurity = true zeigen,
-- und es dürfen nur die beiden Policies oben auftauchen, keine mit "anon" oder "public".
-- ---------------------------------------------------------------------------
-- select tablename, rowsecurity from pg_tables
--   where schemaname='public' and tablename in ('orders','teams');
-- select tablename, policyname, roles, cmd from pg_policies
--   where schemaname='public' and tablename in ('orders','teams');

-- Alte Tabelle aus der ersten Version (eine Zeile mit der ganzen Liste) – bleibt als Reserve stehen.
-- create table if not exists public.meta (id text primary key, json text not null default '[]', updated_at timestamptz default now());
