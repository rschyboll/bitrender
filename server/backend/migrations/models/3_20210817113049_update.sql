-- upgrade --
ALTER TABLE "worker" RENAME COLUMN "secret_key" TO "private_key";
-- downgrade --
ALTER TABLE "worker" RENAME COLUMN "private_key" TO "secret_key";
