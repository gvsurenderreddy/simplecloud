# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

from fabric.api import *
import os.path

project = "simplecloud"

INSTANCE_FOLDER_PATH = "/tmp/instance"

# the user to use for the remote commands
env.user = ''
# the servers where the commands are executed
env.hosts = ['']


def init():
    """
    Reset local debug env.
    """
    local("rm -rf %s" % INSTANCE_FOLDER_PATH)
    local("mkdir %s" % INSTANCE_FOLDER_PATH)
    local("mkdir %s/config" % INSTANCE_FOLDER_PATH)
    local("cp config/kvm.xml %s/config/vm.xml" % INSTANCE_FOLDER_PATH)
    setup()

def setup():
    """
    Setup virtual env.
    """

    local("virtualenv env")
    activate_this = "env/bin/activate_this.py"
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
    if not os.path.exists(INSTANCE_FOLDER_PATH):
	local("mkdir %s" % INSTANCE_FOLDER_PATH)
    local("python manage.py initdb")

def debug():
    """
    Debug.
    """

    init()
    local("python manage.py runserver -t 0.0.0.0")

def d():
    local("rm -rf %s" % INSTANCE_FOLDER_PATH)
    local("mkdir %s" % INSTANCE_FOLDER_PATH)
    local("mkdir %s/config" % INSTANCE_FOLDER_PATH)
    local("cp config/kvm.xml %s/config/vm.xml" % INSTANCE_FOLDER_PATH)
    local("python manage.py initdb")
    local("python manage.py runserver -t 0.0.0.0")

def test():
    """
    Test
    """
    init()
    local("python manage.py inittestdb")

    local("python manage.py runserver -t 0.0.0.0")

def create():
    """
    Get translation file
    """
    local("pybabel extract -F babel.cfg -o messages.pot ./simplecloud")
    local("pybabel init -i messages.pot -d simplecloud/translations -l zh_CN")

def update():
    """
    Update translation file
    """
    local("pybabel extract -F babel.cfg -o messages.pot ./simplecloud")
    local("pybabel update -i messages.pot -d simplecloud/translations")

def build():
    """
    Babel compile.
    """
    #local("pybabel compile -d simplecloud/translations")
    local("python setup.py compile_catalog --directory `find simplecloud/ -name translations` --locale zh_CN -f")
