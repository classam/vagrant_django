#!/bin/bash

echo "Creating Database"
sudo -u postgres createdb 'threepanel';
echo "Creating User"
sudo -u postgres psql --command "CREATE USER threepanel WITH password '$1';"
sudo -u postgres psql --command "ALTER USER threepanel WITH password '$1';"
echo "Granting Privileges to User"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE threepanel TO threepanel;"
