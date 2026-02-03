# Async7 Controller

## DB

```sql
CREATE TABLE IF NOT EXISTS hl7v2
(
    id SERIAL PRIMARY KEY UNIQUE,
    message TEXT NOT NULL,
    group_id TEXT NOT NULL,
    date_received TIMESTAMP NOT NULL DEFAULT NOW(),
    assigned_to TEXT NULL
);

ALTER TABLE hl7v2 ADD COLUMN IF NOT EXISTS message_type TEXT NOT NULL;
ALTER TABLE hl7v2 ALTER COLUMN message_type SET NOT NULL;

ALTER TABLE hl7v2 ADD COLUMN IF NOT EXISTS date_assigned TIMESTAMP NULL;

CREATE INDEX IF NOT EXISTS idx_hl7v2_date_assigned ON hl7v2 USING brin (date_received);
CREATE INDEX IF NOT EXISTS idx_hl7v2_date_assigned ON hl7v2 USING brin (date_assigned);
CREATE INDEX IF NOT EXISTS idx_hl7v2_group_id ON hl7v2 USING btree (group_id);
```
