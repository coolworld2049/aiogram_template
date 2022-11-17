CREATE schema schema;
SET schema 'schema';

CREATE TABLE IF NOT EXISTS schema.user (
    user_id BIGINT PRIMARY KEY NOT NULL UNIQUE,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    "role" TEXT,
    last_seen TIMESTAMP
);


CREATE TABLE IF NOT EXISTS schema.temp (
    user_id BIGINT PRIMARY KEY NOT NULL UNIQUE REFERENCES schema.user(user_id),
    last_message_id TEXT
);

CREATE OR REPLACE FUNCTION schema.upsert_table_temp(us_id BIGINT, l_msg TEXT) RETURNS VOID AS $$
BEGIN
    UPDATE schema.temp SET last_message_id = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO schema.temp VALUES ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION schema.upsert_table_user(us_id BIGINT, "role" TEXT) RETURNS VOID AS $$
BEGIN
    UPDATE schema.user SET "role" = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO schema.user(user_id, "role") VALUES ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;


