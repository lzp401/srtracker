-- Generate temp table to put data from oracle database
CREATE TABLE IF NOT EXISTS {0}
(
  "srNumber" bigserial NOT NULL,
  customer character varying(1024),
  description text,
  "openDate" date,
  "modifiedDate" date,
  "touchDate" date,
  "closeDate" date
);

CREATE TABLE IF NOT EXISTS sync_log
(
    id serial NOT NULL PRIMARY KEY,
    sync_time timestamp with time zone NOT NULL,
    record_synced integer NOT NULL
);
