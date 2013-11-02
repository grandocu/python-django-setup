from fabric.api import lcd, local
import os


def prepare_deployment(branch_name):
    local('python ./grandoenergymodel/manage.py test doe22')
    #I dont' think I need this.  I set up my commits with messages on my own
    #local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

def deploy_branch():
    with lcd(os.path.dirname(__file__)):
        local('git checkout --orphan production')
        local('git rm -rf .')
        local('git pull git@github.com:grandocu/python-django-setup.git')
        local('python ./grandoenergymodel/manage.py migrate doe22')
        local('python ./grandoenergymodel/manage.py test doe22')
        local('python ./grandoenergymodel/manage.py runserver')