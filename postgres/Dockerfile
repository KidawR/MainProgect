FROM postgres:16
COPY init.sql /docker-entrypoint-initdb.d/

COPY migration.sql /docker-entrypoint-initdb.d/02-migration.sql