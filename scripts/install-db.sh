#!/bin/bash

db_host="localhost"
db_port="5432"
db_name="medical_crawler"
db_user="crawler"
db_password="bG9jYWxob3N0"

# Create Database and Tables

create_db_sql="CREATE DATABASE $db_name;"
create_urls_table_sql="CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY, url VARCHAR(2084) UNIQUE, dom JSONB, turn INTEGER DEFAULT 1);"

echo "Creating database: $db_name"
sudo -u postgres psql -c "$create_db_sql" 2>/dev/null || echo "Database $db_name already exists"
echo
echo "Creating urls table"
sudo -u postgres psql -d $db_name -c "$create_urls_table_sql" 2>/dev/null || echo "Table urls already exists"

# Create User Crawler

new_user="crawler"
new_user_password="bG9jYWxob3N0"

create_user_sql="CREATE USER $new_user WITH PASSWORD '$new_user_password';"

echo "Creating user: $new_user"
sudo -u postgres psql -c "$create_user_sql" 2>/dev/null || echo "User $new_user already exists"
echo

# Grant Permissions to User Crawler

grant_permissions_sql="GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"
grant_table_permissions_sql="GRANT ALL PRIVILEGES ON TABLE urls TO $db_user;"
grant_sequence_permissions_sql="GRANT USAGE, SELECT, UPDATE ON SEQUENCE urls_id_seq TO $db_user;"

echo "Granting permissions to user: $db_user"
sudo -u postgres psql -c "$grant_permissions_sql" 2>/dev/null || echo "Failed to grant permissions to user $db_user"
sudo -u postgres psql -d $db_name -c "$grant_table_permissions_sql" 2>/dev/null || echo "Failed to grant table permissions to user $db_user"
sudo -u postgres psql -d $db_name -c "$grant_sequence_permissions_sql" 2>/dev/null || echo "Failed to grant sequence permissions to user $db_user"
echo
