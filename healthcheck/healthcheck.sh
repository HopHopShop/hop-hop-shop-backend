#!/bin/bash

# Проверка подключения к MariaDB
if mysqladmin ping -h localhost -u root -pmy_password >/dev/null 2>&1; then
  echo "MariaDB is up"
else
  echo "MariaDB is down"
  exit 1
fi

# Дополнительная проверка на инициализацию InnoDB
if [[ $(mysql -u root -pmy_password -e "SHOW ENGINE INNODB STATUS;" | grep "initialized") ]]; then
  echo "InnoDB initialized"
else
  echo "InnoDB not initialized"
  exit 1
fi
