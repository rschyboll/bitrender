-- upgrade --
ALTER TABLE "worker" RENAME COLUMN "activated" TO "active";
-- downgrade --
ALTER TABLE "worker" RENAME COLUMN "active" TO "activated";
