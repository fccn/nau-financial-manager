#!/bin/bash
# wait-for-mysql.sh

until mycli -h ${DB_HOST:=nau-database-mysql} --port ${DB_PORT:=3306} -u ${MYSQL_USER:=nau_user} -p ${MYSQL_PASSWORD:=nau_password} -e 'SELECT 1' --myclirc /tmp/.myclirc; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec "$@"
