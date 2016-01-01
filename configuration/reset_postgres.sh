#!/bin/bash

sudo -u postgres dropdb threepanel
sudo -u postgres createdb threepanel
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE threepanel TO threepanel;"
