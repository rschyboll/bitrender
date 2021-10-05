-- upgrade --
CREATE TABLE IF NOT EXISTS "binary" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "version" TEXT NOT NULL,
    "url" TEXT NOT NULL
);
-- downgrade --
DROP TABLE IF EXISTS "binary";
