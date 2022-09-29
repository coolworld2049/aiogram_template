DELETE FROM pg_type WHERE typname = 'user_role';
DELETE FROM pg_type WHERE typname = 'order_state';

CREATE TYPE base_role AS ENUM ('customer', 'contractor');
CREATE TYPE order_state AS ENUM (
            'OrderStates:order_start_creating',
            'OrderStates:order_accepted',
            'OrderStates:order_in_work',
            'OrderStates:order_completed',
            'OrderStates:order_terminated'
        );

CREATE TABLE IF NOT EXISTS bot.user (
   user_id BIGINT PRIMARY KEY,
   username TEXT,
   first_name TEXT,
   last_name TEXT,
   agree_with_rules BOOLEAN,
   phone TEXT,
   is_admin BOOLEAN,
   last_seen FLOAT
);

CREATE TABLE IF NOT EXISTS bot.customer (
   user_id BIGINT PRIMARY KEY REFERENCES bot.user(user_id),
   state TEXT,
   completed_orders_id TEXT,
   number_completed_orders INTEGER DEFAULT 0,
   last_seen FLOAT
);

CREATE TABLE IF NOT EXISTS bot.contractor (
   user_id BIGINT PRIMARY KEY REFERENCES bot.user(user_id),
   state TEXT,
   completed_deliveries_id TEXT,
   number_completed_orders INTEGER DEFAULT 0,
   last_seen FLOAT
);


CREATE TABLE IF NOT EXISTS bot.order (
   id BIGINT PRIMARY KEY,
   contractor_id  BIGINT REFERENCES bot.user(user_id) NULL,
   customer_id  BIGINT REFERENCES bot.user(user_id) NULL,
   "role" base_role,
   state order_state,
   create_time FLOAT
);

CREATE TABLE IF NOT EXISTS bot.temp (
   user_id BIGINT PRIMARY KEY,
   last_message_id TEXT
);

CREATE OR REPLACE FUNCTION bot.upsert_table_temp(us_id BIGINT, l_msg TEXT) RETURNS VOID AS $$
BEGIN
    UPDATE bot.temp SET last_message_id = $2 WHERE user_id = $1;
    IF NOT FOUND THEN
        INSERT INTO bot.temp values ($1, $2);
    END IF;
END;
$$
LANGUAGE plpgsql;