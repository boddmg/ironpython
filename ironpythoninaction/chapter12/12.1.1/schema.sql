CREATE DATABASE ironpython_in_action;

\connect ironpython_in_action

CREATE SEQUENCE person_id_seq START 1 INCREMENT 1;

CREATE TABLE person
(
  id int4 NOT NULL DEFAULT nextval('person_id_seq'),
  name varchar(100) NOT NULL,
  directed_count int4 NULL,
  CONSTRAINT person_pkey PRIMARY KEY (id)
);

CREATE SEQUENCE movie_id_seq START 1 INCREMENT 1;

CREATE TABLE movie
(
  id int4 NOT NULL DEFAULT nextval('movie_id_seq'),
  title varchar(100) NOT NULL,
  released timestamp,
  director_id int4 NOT NULL,
  CONSTRAINT movie_pkey PRIMARY KEY (id),
  CONSTRAINT movie_person_fkey FOREIGN KEY (director_id)
      REFERENCES person (id)
);

CREATE SEQUENCE role_id_seq START 1 INCREMENT 1;

CREATE TABLE role
(
  id int4 NOT NULL DEFAULT nextval('role_id_seq'),
  movie_id int4 NOT NULL,
  person_id int4 NOT NULL,
  character varchar(100) NOT NULL,
  CONSTRAINT role_pkey PRIMARY KEY (id),
  CONSTRAINT role_movie_fkey FOREIGN KEY (movie_id)
      REFERENCES movie (id),
  CONSTRAINT role_person_fkey FOREIGN KEY (person_id)
      REFERENCES person (id)
);


insert into person(name) values ('David Fincher');
insert into person(name) values ('Edward Norton');
insert into person(name) values ('Brad Pitt');
insert into person(name) values ('Meat Loaf');
insert into person(name) values ('Morgan Freeman');
insert into person(name) values ('Kevin Spacey');
insert into person(name) values ('Spike Jonze');
insert into person(name) values ('John Cusack');
insert into person(name) values ('John Malkovich');
insert into person(name) values ('Cameron Diaz');
insert into person(name) values ('Rian Johnson');
insert into person(name) values ('Joseph Gordon-Levitt');
insert into person(name) values ('Nora Zehetner');
insert into person(name) values ('Lukas Haas');
insert into person(name) values ('Curtis Hanson');
insert into person(name) values ('Russell Crowe');
insert into person(name) values ('James Cromwell');


insert into movie (title, released, director_id)
select 'Fight Club', '1999-10-15', id
from person where name = 'David Fincher';

insert into movie(title, released, director_id)
select 'Se7en', '1996-01-05', id
from person where name = 'David Fincher';

insert into movie(title, released, director_id)
select 'Being John Malkovich', '2000-03-17', id
from person where name = 'Spike Jonze';

insert into movie(title, released, director_id)
select 'Brick', '2006-05-21', id
from person where name = 'Rian Johnson';

insert into movie(title, released, director_id)
select 'LA Confidential', '1997-10-31', id
from person where name = 'Curtis Hanson';

insert into role(character, person_id, movie_id)
select 'Narrator', p.id, m.id
from person p, movie m
where p.name = 'Edward Norton'
and m.title = 'Fight Club';

insert into role(character, person_id, movie_id)
select 'Tyler Durden', p.id, m.id
from person p, movie m
where p.name = 'Brad Pitt'
and m.title = 'Fight Club';

insert into role(character, person_id, movie_id)
select 'Robert Paulsen', p.id, m.id
from person p, movie m
where p.name = 'Meat Loaf'
and m.title = 'Fight Club';

insert into role(character, person_id, movie_id)
select 'David Mills', p.id, m.id
from person p, movie m
where p.name = 'Brad Pitt'
and m.title = 'Se7en';

insert into role(character, person_id, movie_id)
select 'William Somerset', p.id, m.id
from person p, movie m
where p.name = 'Morgan Freeman'
and m.title = 'Se7en';

insert into role(character, person_id, movie_id)
select 'John Doe', p.id, m.id
from person p, movie m
where p.name = 'Kevin Spacey'
and m.title = 'Se7en';

insert into role(character, person_id, movie_id)
select 'Craig Schwartz', p.id, m.id
from person p, movie m
where p.name = 'John Cusack'
and m.title = 'Being John Malkovich';

insert into role(character, person_id, movie_id)
select 'Lotte Schwartz', p.id, m.id
from person p, movie m
where p.name = 'Cameron Diaz'
and m.title = 'Being John Malkovich';

insert into role(character, person_id, movie_id)
select 'John Malkovich', p.id, m.id
from person p, movie m
where p.name = 'John Malkovich'
and m.title = 'Being John Malkovich';

insert into role(character, person_id, movie_id)
select 'Christopher Bing', p.id, m.id
from person p, movie m
where p.name = 'David Fincher'
and m.title = 'Being John Malkovich';

insert into role(character, person_id, movie_id)
select 'Brendan Frye', p.id, m.id
from person p, movie m
where p.name = 'Joseph Gordon-Levitt'
and m.title = 'Brick';

insert into role(character, person_id, movie_id)
select 'Laura', p.id, m.id
from person p, movie m
where p.name = 'Nora Zehetner'
and m.title = 'Brick';

insert into role(character, person_id, movie_id)
select 'The Pin', p.id, m.id
from person p, movie m
where p.name = 'Lukas Haas'
and m.title = 'Brick';

insert into role(character, person_id, movie_id)
select 'Jack Vincennes', p.id, m.id
from person p, movie m
where p.name = 'Kevin Spacey'
and m.title = 'LA Confidential';

insert into role(character, person_id, movie_id)
select 'Bud White', p.id, m.id
from person p, movie m
where p.name = 'Russell Crowe'
and m.title = 'LA Confidential';

insert into role(character, person_id, movie_id)
select 'Dudley Smith', p.id, m.id
from person p, movie m
where p.name = 'James Cromwell'
and m.title = 'LA Confidential';


