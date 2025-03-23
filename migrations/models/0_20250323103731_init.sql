-- upgrade --
CREATE TABLE IF NOT EXISTS "tokendb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(75) NOT NULL,
    "user_id" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "userdb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(75) NOT NULL,
    "password" VARCHAR(75) NOT NULL,
    "mail" VARCHAR(75) NOT NULL,
    "year_of_birth" INT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
