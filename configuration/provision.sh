#!/bin/bash

export VIRTUALENV=$HOME/threepanel_environment
echo "Home: $HOME"
echo "Virtualenv: $VIRTUALENV"

sudo apt-get -y update
sudo apt-get -y upgrade

echo 'Install Dev Tools'
sudo apt-get install -y ack-grep vim dos2unix


echo "Modify the .bashrc"
echo "export PYTHONPATH=$HOME/threepanel/threepanel" >> $HOME/.bashrc
echo "source $VIRTUALENV/bin/activate" >> $HOME/.bashrc
echo "alias dj='python3 $HOME/threepanel/threepanel/manage.py'" >> $HOME/.bashrc
echo "alias in='cd $HOME/threepanel/ && invoke'" >> $HOME/.bashrc


echo "Install Redis"
sudo apt-get install -y redis-server

echo "Install PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib libpq-dev

echo "Install NGINX"
sudo apt-get install -y nginx

echo "Install Python"
sudo apt-get install -y python3 python3-dev python3-venv

echo "Create a Virtual Environment, Install Pip & Python Dependencies"
mkdir $VIRTUALENV
pyvenv $VIRTUALENV
source $VIRTUALENV/bin/activate && pip install -r $HOME/threepanel/configuration/requirements.txt

rm /etc/nginx/sites-enabled/default

mkdir $HOME/logs
