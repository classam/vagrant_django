#!/bin/bash

mkdir $HOME/db_backups
sudo -u postgres pg_dump ${project_slug} > $HOME/db_backups/`date +"%Y-%m-%d-%s"`.db_backup
