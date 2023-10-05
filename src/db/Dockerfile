# DockerFile to build my sql image

FROM mysql:latest

EXPOSE 3306

ADD init.sql /docker-entrypoint-initdb.d/init.sql
