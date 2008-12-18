-- run with:
-- psql -f postgres.sql -U postgres postgres

create database twatter_db;

\connect twatter_db

create table friends (
  id integer primary key,
  screen_name varchar(100),
  name varchar(100),
  description varchar(1000),
  location varchar(200),
  url varchar(1000),
  image_url varchar(1000)
);

create table tweets (
  id integer primary key,
  created timestamp,
  text varchar(200),
  friend_id integer references friends (id)
);

