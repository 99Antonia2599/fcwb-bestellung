-- FCWB Materialbestellung – Datenbank (Stand 09.09.2026)
-- Im Supabase SQL Editor einfügen und ausführen. Mehrfach ausführbar.

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

-- Zugriff für alle mit dem publishable Key (internes Vereinstool)
alter table public.orders enable row level security;
alter table public.teams  enable row level security;
drop policy if exists "orders_all" on public.orders;
drop policy if exists "teams_all"  on public.teams;
create policy "orders_all" on public.orders for all using (true) with check (true);
create policy "teams_all"  on public.teams  for all using (true) with check (true);

-- Live-Sync
alter publication supabase_realtime add table public.orders;
alter publication supabase_realtime add table public.teams;

-- Alte Tabelle aus der ersten Version (eine Zeile mit der ganzen Liste) – bleibt als Reserve stehen.
-- create table if not exists public.meta (id text primary key, json text not null default '[]', updated_at timestamptz default now());
