-- upgrade --
ALTER TABLE "worker" DROP COLUMN "private_key";
-- downgrade --
ALTER TABLE "worker" ADD "private_key" BYTEA NOT NULL;
