# -*- coding: utf-8 -*-

import sys, os, pwd

project = "simplecloud"

# Use instance folder, instead of env variables.
# specify dev/production config
#os.environ['%s_APP_CONFIG' % project.upper()] = ''
# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
#os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir

BASE_DIR = os.path.join(os.path.dirname(__file__))
# activate virtualenv
activate_this = os.path.join(BASE_DIR, "env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# give wsgi the "application"
from simplecloud import create_app
application = create_app()

# Add following lines to /etc/apache2/sites-available/simplecloud file
#<VirtualHost *>
#    ServerName example.com
#
#    WSGIDaemonProcess simplecloud user=simplecloud group=simplecloud threads=5
#    WSGIScriptAlias / /var/www/simplecloud/app.wsgi
#
#    <Directory /var/www/simplecloud>
#        WSGIProcessGroup simplecloud
#        WSGIApplicationGroup %{GLOBAL}
#        Order deny,allow
#        Allow from all
#    </Directory>
#</VirtualHost>
