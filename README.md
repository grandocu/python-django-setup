python-django-setup
===================

Set up for django projects with virtualenvwrapper and fabric


This assumes you have installed python2.7, pip, and easy_install.  I'm a beginner so take it easy on me.  Most of this is taken from a blog I
found (http://www.jeffknupp.com/blog/2012/02/09/starting-a-django-project-the-right-way/),  I've made some small changes for my setup.

You will need to get virtualenvwrapper

    pip install virtualenvwrapper

Then you will have to set your $WORKON_HOME envrionment variable.  Here is where I start to diverge from the online tutorials.  I make a folder inside my project called Envs.

    mkdir -p PROJECT_DIR/Envs

Then you set your $WORKON_HOME in your ~/.bash_profile and source the virtualenvwrapper.sh

    export WORKON_HOME=$HOME/PROJECT_DIR/Envs
    source /usr/local/bin/virtualenvwrapper.sh

Make sure to source your bash profile

    source ~/.bash_profile

Create a virutal environment

    mkvirtualenv env

Initialize your git project 

    git init .
    git add .
    git commite -m"Initial commit"

For cross platform development I will make a 'envwindows' and so on.

Now you can install django, django-extensions, south for migrations, and fabric for deployment

    pip install Django
    pip install django-extensions
    pip install south
    pip install fabric

This is where we start our project and app

    django-addmin.py startproject myproject
    cd myproject
    python manage.py startapp myapp

Set up your database engine and name.  There are different setups so an online search will guide you on this step.
For now I'll just setup an sqlite3 database

    import os
    #Set base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    #.... code here .....


    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),


Add 'myapp' and 'django_extensions' as an INSTALLED_APP in your settings.py, synce your db and migrate

    python manage.py syncdb
    cd myappc
    python manage.py schemamigration myapp --init

When changes are made, run:
    python manage.py schemamigration myapp --auto


So far there are two actions I like to make for my fabfile.  So create one now

    touch fabfile.py

The first action I include runs the tests in your project and then merges the last commit of the current branch you are in
to the master branch

````
from fabric.api import lcd, local
import os


def prepare_deployment(branch_name):
    local('python ./myproject/manage.py test myapp')
    local('git checkout master && git merge ' + branch_name)
````

you execute this with

    fab prepare_deployment:<branch_name>

The next action I like to do is a deploy_production where I create a new orphaned branch, remove all the files, and pull from the
remote repository.  I then migrate, test, and run the server.  Make sure to set up your ssh key access to your github repository.

````
def deploy_branch():
    with lcd(os.path.dirname(__file__)):
        local('git checkout --orphan production')
        local('git rm -rf .')
        local('git pull git@github.com:grandocu/python-django-setup.git')
        local('python ./myproject/manage.py migrate myapp')
        local('python ./myproject/manage.py test myapp')
        local('python ./myproject/manage.py runserver')
````

Now when you run:

    fab deploy_branch

You will be on a 'production' branch and the sever should be started.