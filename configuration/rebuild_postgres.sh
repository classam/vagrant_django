#!/bin/bash

mkdir $HOME/db_backups
sudo -u postgres psql -d threepanel -f $1
