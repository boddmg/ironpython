
-- run with:
-- sqlite3 -init sqlite.sql <db filename>

create table friends (
  id integer primary key,
  screen_name text,
  name text,
  description text,
  location text,
  url text,
  image_url text
);

create table tweets (
  id integer,
  created text,
  text text,
  friend_id integer
);

