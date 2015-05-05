-- Update existing rows in record table
UPDATE recordlist_record
SET
  customer = {0}.customer,
  description = {0}.description,
  "openDate" = {0}."openDate",
  "modifiedDate" = {0}."modifiedDate",
  "touchDate" = {0}."touchDate",
  "closeDate" = {0}."closeDate"
FROM {0}
WHERE recordlist_record."srNumber" = {0}."srNumber";

-- Insert new rows from source database
INSERT INTO recordlist_record("srNumber", customer, description, "openDate", "modifiedDate", "touchDate", "closeDate", "calPriority")
SELECT *, 3 FROM {0}
WHERE {0}."srNumber" NOT IN (SELECT distinct "srNumber" FROM recordlist_record WHERE "srNumber" != null);

-- Mark updated data as review required
UPDATE recordlist_record
SET "reviewRequired" = true
FROM {0}
WHERE recordlist_record."srNumber" = {0}."srNumber";

INSERT INTO sync_log(sync_time, record_synced) VALUES (CURRENT_TIMESTAMP, (SELECT COUNT(*) FROM {0}));

-- Delete temp table
DROP TABLE {0};
