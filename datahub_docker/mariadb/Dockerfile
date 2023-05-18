FROM mariadb:10.5.8

ADD ./init.sql /docker-entrypoint-initdb.d/
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/init.sql
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["mysqld", "--character-set-server=utf8mb4", "--collation-server=utf8mb4_bin", "--default-authentication-plugin=mysql_native_password"]