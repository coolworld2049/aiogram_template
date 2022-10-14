-- CREATE schema schema;
-- SET schema 'schema';

DELETE FROM pg_type WHERE typname = 'base_role';
DELETE FROM pg_type WHERE typname = 'user_state';

CREATE TYPE base_role AS ENUM ('customer', 'contractor', 'admin');
CREATE TYPE user_state AS ENUM (
            'UserStates:creating',
            'UserStates:accepted',
            'UserStates:progress',
            'UserStates:completed',
            'UserStates:terminated'
        );

CREATE TABLE IF NOT EXISTS schema.user (
   user_id BIGINT PRIMARY KEY NOT NULL UNIQUE,
   username TEXT,
   first_name TEXT,
   last_name TEXT,
   state user_state,
   "role" base_role,
   is_admin BOOLEAN,
   is_manager BOOLEAN,
   last_seen FLOAT
);


CREATE TABLE IF NOT EXISTS schema.order (
   id BIGINT PRIMARY KEY,
   contractor_id  BIGINT REFERENCES schema.user(user_id) NULL,
   customer_id  BIGINT REFERENCES schema.user(user_id) NULL,
   state user_state,
   create_time FLOAT
);

CREATE TABLE IF NOT EXISTS schema.temp (
   user_id BIGINT PRIMARY KEY REFERENCES schema.user(user_id),
   last_message_id TEXT
);

CREATE OR REPLACE FUNCTION schema.upsert_table_temp(us_id BIGINT, l_msg TEXT) RETURNS VOID AS $$
BEGIN
    UPDATE schema.temp SET last_message_id = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO schema.temp values ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION schema.upsert_table_user(us_id BIGINT, is_admin BOOLEAN) RETURNS VOID AS $$
BEGIN
    UPDATE schema.user SET is_admin = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO schema.user values ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;