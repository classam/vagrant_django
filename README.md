
Install
-------
This ball of scripts will scaffold a completely operational Django environment including Redis and Postgres.
Here's how it works.

1. Fork this repo.

2. Install VirtualBox

3. Install Vagrant

4. Command Line (from this repository's folder)

    $> vagrant up

    $> vagrant ssh

    $> source django_environment/bin/activate

    $> cd vagrant_django

    $> django-admin startproject butterbutt

    $> cd butterbutt

    $> ./manage.py startapp dashboard

    $> cd ..

    $> sudo python3 configuration/install.py

    $> dj migrate

