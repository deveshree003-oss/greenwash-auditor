-- Supabase schema for Greenwash Auditor
-- Run this in your Supabase SQL editor or psql to create the reports table.

create table if not exists reports (
  id text primary key,
  report jsonb not null,
  created_at timestamptz default now()
);

-- Optional index for created_at if you plan to query by time
create index if not exists reports_created_at_idx on reports (created_at desc);

-- Optional table to track uploaded files (metadata only). PDFs are stored in
-- Supabase Storage; this table helps mapping files to reports and storing
-- friendly URLs.
create table if not exists files (
  id text primary key,
  report_id text references reports(id) on delete cascade,
  bucket text not null,
  path text not null,
  public_url text,
  created_at timestamptz default now()
);

create index if not exists files_report_id_idx on files (report_id);
