-- upgrade --
CREATE TABLE IF NOT EXISTS "task" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" TEXT NOT NULL,
    "engine" TEXT NOT NULL,
    "samples" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
