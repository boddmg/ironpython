-- run with SQL Server Management Studio
use master;

create database twatter_db;
go

use twatter_db;

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
  created datetime,
  text varchar(200),
  friend_id integer references friends (id)
);

