# Use the official PostgreSQL image
FROM postgres:latest

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=Kennwort1
ENV POSTGRES_DB=postgres

COPY create_db.sql /docker-entrypoint-initdb.d/schema.sql

EXPOSE 5432
