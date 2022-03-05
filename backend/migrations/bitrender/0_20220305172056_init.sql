-- upgrade --
CREATE TABLE IF NOT EXISTS "role" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" TEXT NOT NULL,
    "initial" BOOL NOT NULL
);
COMMENT ON TABLE "role" IS 'Database model describing a user role.';
CREATE TABLE IF NOT EXISTS "rolehaspermission" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "permission" SMALLINT NOT NULL,
    "initial" BOOL NOT NULL,
    "role_id" UUID NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "rolehaspermission"."permission" IS 'READ_TASKS: 1\nADD_TASKS: 2\nREMOVE_TASKS: 3';
COMMENT ON TABLE "rolehaspermission" IS 'Database model describing permissions assigned to a specific user role.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
