CREATE DATABASE "online_university_db_2" ;

CREATE USER "online_university_user2" WITH PASSWORD 'Q-V3dGx8RkKKoMwwHYO06aRglj06_V_p02cE1n7fGYQ' ;

ALTER ROLE "online_university_user2" SET client_encoding TO 'utf8' ;

ALTER ROLE "online_university_user2" SET default_transaction_isolation TO 'read committed' ;

ALTER ROLE "online_university_user2" SET timezone TO 'UTC' ;

ALTER USER "online_university_user2" CREATEDB ;


SELECT has_schema_privilege( 'online_university_user2','public','CREATE') ;

ALTER DATABASE "online_university_db_2" OWNER TO "online_university_user2" ;
