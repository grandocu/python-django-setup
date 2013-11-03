from fabric.api import lcd, local
import os


def prepare_deployment(branch_name):
    local('python ./myproject/manage.py test myapp')
    #I dont' think I need this.  I set up my commits with messages on my own
    #local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

def deploy_branch():
    with lcd(os.path.dirname(__file__)):
        local('git checkout --orphan production')
        #Remove non-fabfile and non-git directories
        local('git rm -rf ./myproject')
        local('git pull git@github.com:grandocu/python-django-setup.git')
        local('python ./myproject/manage.py migrate myapp')
        local('python ./myproject/manage.py test myapp')
        local('python ./myproject/manage.py runserver')