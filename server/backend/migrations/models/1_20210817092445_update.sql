-- upgrade --
CREATE TABLE IF NOT EXISTS "worker" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" TEXT NOT NULL,
    "secret_key" BYTEA NOT NULL,
    "register_date" DATE NOT NULL,
    "last_active_date" DATE,
    "activated" BOOL NOT NULL  DEFAULT False
);
-- downgrade --
DROP TABLE IF EXISTS "worker";
