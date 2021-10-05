-- upgrade --
ALTER TABLE "worker" ALTER COLUMN "register_date" TYPE TIMESTAMPTZ USING "register_date"::TIMESTAMPTZ;
-- downgrade --
ALTER TABLE "worker" ALTER COLUMN "register_date" TYPE DATE USING "register_date"::DATE;
