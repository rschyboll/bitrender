-- upgrade --
ALTER TABLE "worker" DROP COLUMN "last_active_date";
-- downgrade --
ALTER TABLE "worker" ADD "last_active_date" DATE;
