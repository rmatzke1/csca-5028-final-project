create database movie_recaps_dev;
create database movie_recaps_test;

create user db_user with password 'password';
grant all privileges on database movie_recaps_dev to db_user;
grant all privileges on database movie_recaps_test to db_user;
