#!/bin/bash

db_host="localhost"
db_port="5432"
db_name="medical_crawler"
db_user="crawler"
db_password="bG9jYWxob3N0"

# Drop User Crawler

drop_user_sql="DROP USER IF EXISTS $db_user;"

echo "Dropping user: $db_user"
sudo -u postgres psql -c "$drop_user_sql" 2>/dev/null && echo "User $db_user has been dropped" || echo "User $db_user does not exist"
echo

# Drop Database and Tables

drop_db_sql="DROP DATABASE IF EXISTS $db_name;"
drop_urls_table_sql="DROP TABLE IF EXISTS urls;"
drop_doms_table_sql="DROP TABLE IF EXISTS doms;"

echo "Dropping database: $db_name"
sudo -u postgres psql -c "$drop_db_sql" 2>/dev/null && echo "Database $db_name has been dropped" || echo "Database $db_name does not exist"
echo
echo "Dropping urls table"
sudo -u postgres psql -c "$drop_urls_table_sql" 2>/dev/null && echo "Table urls has been dropped" || echo "Table urls does not exist"
echo
echo "Dropping doms table"
sudo -u postgres psql -c "$drop_doms_table_sql" 2>/dev/null && echo "Table doms has been dropped" || echo "Table doms does not exist"