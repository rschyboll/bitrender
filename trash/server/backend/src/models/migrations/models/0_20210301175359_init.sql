-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(32) NOT NULL,
    "password_hash" BYTEA NOT NULL,
    "email" VARCHAR(64) NOT NULL,
    "register_date" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "users" IS 'User Model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
