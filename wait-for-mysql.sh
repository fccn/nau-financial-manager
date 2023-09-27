#!/bin/bash
# wait-for-mysql.sh

until mycli -h $DB_HOST -u $MYSQL_USER -p $MYSQL_PASSWORD -e 'SELECT 1' --myclirc /tmp/.myclirc; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec "$@"
