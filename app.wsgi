activate_this = '/var/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys,os
sys.path.insert(0,'/var/voylla_api')
os.environ['DATABASE_URL'] = "postgresql://voylla:everything@localhost/voylla_development_api"
os.environ['APP_SETTINGS'] = "config.DevelopmentConfig"
os.environ['APP_DATABASE_URL'] = "postgres://voylla@db03.voylla.com/voylla_production"
from app import app as application