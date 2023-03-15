CREATE DATABASE bet_maker;

CREATE SCHEMA bet_maker_content;

SET search_path TO bet_maker_content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE bet (
    id UUID PRIMARY KEY,
    event_id UUID,
    value NUMERIC(20, 2) CONSTRAINT check_value_is_positive CHECK (value > 0)
);

CREATE TYPE event_state AS ENUM ('NEW', 'FINISHED_WIN', 'FINISHED_LOOSE');

CREATE TABLE event (
    id UUID PRIMARY KEY,
    state event_state,
    deadline INTEGER
);