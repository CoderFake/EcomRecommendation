#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."
until mysqladmin ping -h"localhost" --silent; do
    sleep 1
done

echo "Setting up databases..."
mysql -u root -p${MYSQL_ROOT_PASSWORD} <<-EOSQL
    CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

    CREATE DATABASE IF NOT EXISTS test_${MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    GRANT ALL PRIVILEGES ON test_${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

    FLUSH PRIVILEGES;
EOSQL

echo "MySQL setup completed."