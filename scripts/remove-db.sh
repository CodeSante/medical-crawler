#!/bin/bash

db_host="localhost"
db_port="5432"
db_name="medical_crawler"
db_user="crawler"

# Drop Database and Tables

drop_db_sql="DROP DATABASE IF EXISTS $db_name;"
drop_urls_table_sql="DROP TABLE IF EXISTS urls;"

echo "Dropping database: $db_name"
sudo -u postgres psql -c "$drop_urls_table_sql" -d $db_name 2>/dev/null || echo "Failed to drop urls table"
sudo -u postgres psql -c "$drop_db_sql" 2>/dev/null || echo "Failed to drop database $db_name"
echo

echo "Script execution completed."