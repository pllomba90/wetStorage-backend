-- First, drop the tables if they exist
DROP TABLE IF EXISTS "downriver_storage";
DROP TABLE IF EXISTS "bin";
DROP TABLE IF EXISTS "grade";

CREATE TABLE "grades" (
  "name" VARCHAR PRIMARY KEY,
  "density" INT
);


