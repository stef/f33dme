import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 

os.environ['DJANGO_SETTINGS_MODULE'] = 'f33dme.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Apache sites-enabled config:
#
# WSGIScriptAlias /pippi_url "/path/to/your/f33dme/apache/django.wsgi"
# Alias /f33dme_url_prefix/media "/path/to/your/f33dme/media"
# <Directory "/path/to/your/f33dme">
#     Options FollowSymLinks
#     AllowOverride All
# </Directory>
