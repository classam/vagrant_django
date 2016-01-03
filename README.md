
Install
-------
This ball of scripts will scaffold a completely operational Django environment including Redis and Postgres.
Here's how it works.

1. Fork this repo. This will be the repo for your own project. Give it a good name. A good name like "butterbutt". That's a really good name.

2. Clone your forked repo to your computer.

3. Install VirtualBox

4. Install Vagrant

5. Command Line (from this repository's folder)

    $> vagrant up

    $> vagrant ssh

    $> source django_environment/bin/activate

    $> cd vagrant_django

    $> django-admin startproject butterbutt

    $> cd butterbutt

    $> ./manage.py startapp dashboard

    $> cd ..

    $> sudo python3 configuration/install.py

5. Add your new django project to the git repo.

6. Update the following text to be your own readme, delete everything from this point up, and commit.

ButterButt
----------

This is my Django project for putting butter on butts.
If you want to run it on your own computer, do the following:

1. Clone this repo to your computer.

2. Install VirtualBox

3. Install Vagrant

4. Command Line (from this repository's folder)

    $> vagrant up

    $> vagrant ssh

    $> cd vagrant_django

    $> sudo python3 configuration/install.py

    $> dj migrate

    $> in dev_start

Production
==========

If you want to run it in production, do the following:

1. Create a fresh Ubuntu Vivid Vervet VM. (Try DigitalOcean, they'll make one for you)

2. Clone this repo to "$HOME/vagrant_django"

3. Command Line (from this repository's folder)

    $> cd vagrant_django

    $> sudo ./configuration/provision.sh

    $> sudo python3 configuration/install.py

    $> dj migrate

    $> in prod_start
