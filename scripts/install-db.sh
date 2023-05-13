#!/bin/bash

db_host="localhost"
db_port="5432"
db_name="medical_crawler"
db_user="crawler"
db_password="bG9jYWxob3N0"

# Create User Crawler

new_user="crawler"
new_user_password="bG9jYWxob3N0"

create_user_sql="CREATE USER $new_user WITH PASSWORD '$new_user_password';"

echo "Creating user: $new_user"
sudo -u postgres psql -c "$create_user_sql" 2>/dev/null || echo "User $new_user already exists"
echo

# Create Database and Tables

create_db_sql="CREATE DATABASE $db_name;"
create_urls_table_sql="CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY, url TEXT, dom_id INTEGER);"
create_doms_table_sql="CREATE TABLE IF NOT EXISTS doms (id SERIAL PRIMARY KEY, dom_json JSONB, url_id INTEGER);"

echo "Creating database: $db_name"
sudo -u postgres psql -c "$create_db_sql" 2>/dev/null || echo "Database $db_name already exists"
echo
echo "Creating urls table"
sudo -u postgres psql -d $db_name -c "$create_urls_table_sql" 2>/dev/null || echo "Table urls already exists"
echo
echo "Creating doms table"
sudo -u postgres psql -d $db_name -c "$create_doms_table_sql" 2>/dev/null || echo "Table doms already exists"