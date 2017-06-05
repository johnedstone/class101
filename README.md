## class101
Simple python django application tutorial leading to deploying on Openshift

This demo is written for working from a RHEL7 client, python 2.7.x and eventually the openshift client. You can also do this on a Mac, and for the not-so-faint-of heart on a Windows machine.  At no time will you need to be a superuser.  You can also start developing with a free account at pythonanywhere.com


### Prework for Week #1

Nice to have (but not required):

* Create a public Github repo, e.g. class101
* Create your ssh keys, e.g. id_rsa_git and id_rsa_git.pub
* Add your public key to Git (Settings -> SSH and GPG keys)
* Add this stanza to your ~/.ssh/config

```
Host github.com
User <your github user>
IdentityFile ~/.ssh/id_rsa_git
ForwardX11 no
```

* Test your github ssh keys

```
ssh -T git@github.com
You've successfully authenticated, but GitHub does not provide shell access.
```

* \[Windows] or, instead of SSH and SSH keys, can use Windows credential manager with git.exe; if so, no need to test the `ssh -T git@github.com` command above

### Notes on python
Python is space sensitive.  To make your life easier, and to follow recommended style

* Don't use tabs
* Indent 4 spaces
* To facilate this add this line to your `~/.vimrc`:

```
set ai et ts=4 sw=4 sts=4 nu ru

# Or, put this one line here
set modeline
# and add a line to each file as shown here

```


### Week #1
What will be covered:

* discussion on modern web development - no cgi-bin, no raw sql queries, but frameworks (ror, django, cakephp, catalyst, node/express, java?)
* MVC, SOC, DRY, uncoupling, ORM
* Why PaaS (Openshift, Heroku)
* Examples of current customers: nodejs (new development), php (brought in legacy app), others

```
>>> from dashboard.models import BuildConfig as BC
>>> from datetime import date, timedelta
>>>
>>> t = date.today()
>>> t
datetime.date(2017, 5, 8)
>>>
>>> y = t - timedelta(days=1)
>>> y
datetime.date(2017, 5, 7)
>>>
>>> BC.objects.filter(last_seen__lt=y).count()
0
>>> BC.objects.filter(last_seen__gt=y).count()
150

```

```
oc login
oc get pods

NAME                       READY     STATUS    RESTARTS   AGE
parse-image-data-1-grbi1   1/1       Running   0          3d
postgresql-1-e72f2         1/1       Running   0          3d
project.celery-1-1p7u7     1/1       Running   0          3d
redis-1-3504l              1/1       Running   0          3d
```



#### Getting started
* setup python on RHEL7 (on windows or free pythonanywhere account left to the user)
* Reference: https://docs.djangoproject.com/en/1.11/intro/tutorial01/

```
# This is an example - use your git, not mine, your username, etc., etc.
git clone git@github.com:johnedstone/class101.git
# Or, to clone via https (Like, say, without SSH keys set up; and, this example is on Windows):
git clone https://github.com/johnedstone/class101.git C:\temp\modwebdev_class101
cd class101
git config user.name "johnedstone"
git config user.email "johnedstone@gmail.com"
git config push.default simple

## if you do not yet have "virtualenv" package installed, install via pip:
pip install virtualenv --proxy <fqdn:port>

## Note: make the ~/.virtualenvs dir if it does not already exist
virtualenv ~/.virtualenvs/class101
## on *nix:
source ~/.virtualenvs/class101/bin/activate
## or, on Windows (in PowerShell):
. ~\.virtualenvs\class101\Scripts\activate.ps1
pip install pip --proxy <fqdn:port> --upgrade
deactivate

## on *nix:
source ~/.virtualenvs/class101/bin/activate
## or, on Windows (in PowerShell):
. ~\.virtualenvs\class101\Scripts\activate.ps1
pip install --proxy <fqdn:port> django
pip freeze

pwd
  ~/class101

rm -rf project/

# https://docs.djangoproject.com/en/1.11/intro/tutorial01/
django-admin startproject project

ls project/
manage.py  project

ls project/project/
__init__.py  settings.py  urls.py  wsgi.py

echo '# Using python 2.7.5' > project/requirements.txt
echo 'Django==1.11.1' >> project/requirements.txt

cd project
pwd
~/class101/project

python manage.py runserver
# Log into to your server from elsewhere with ssh -x -C -L 8000:127.0.0.1:8000
# and then request from browser http://127.0.0.1:8000

# Alternative, edit project/project/settings and set ALLOWED_HOST = ['*']
python manage.py runserver 0.0.0.0:8000
# request from browser http://fqdn:8000

git branch -a
git remote -v
git status
git add .
git commit -m 'my first commit'
# git commit -am 'my first commit'
git push origin master
# git push
```


### Week #2
* The assumption is that you at least have your virtual environment set up from week #1
* We will discuss
    * From Week #1: remove db.sqlite3 and add to .gitignore: https://github.com/github/gitignore
        ```
        # At least do this
        shell> pwd
        ~/class101

        shell> echo '*pyc' >> .gitignore
        shell> echo 'db.sqlite3' >> .gitignore

        # Maybe this
        shell> git rm -f project/project/*.pyc
        shell> git rm -f project/db.sqlite3
        shell> git add .gitignore
        shell> git status
        
        ```
    * From Week #1: talk about 2x ROR and languages in OSP
    * From Week #1: talk about port 8000 for those on a shared server
    * From Week #1: Let's get clear on these different concepts: .virtualenv (python), git, django-admin startproject project
    * From Week #1: Woo Hoo, 'I have a web server' - everything inside (code) get's handed to PaaS (in the end)

* This week we will
    * look at the `project/project/settings.py`:
    * database
    * other stuff


```
# Where were we from last week
shell> source ~/.virtualenvs/class101/bin/activate

shell> pwd
~/class101

shell> ls -a
.  ..  .git  .gitignore  project  README.md

# If you want to start over, then remove your project.
# Otherwise skip down to 'If there is no need to start over'
shell> rm -rf project/

shell> django-admin startproject project
shell> pwd
~/class101

shell> ls
project  README.md

shell> cd project/

shell> pip freeze
Django==1.11.1
pytz==2017.2

shell> pwd
~/class101/project

shell> ls
manage.py  project

shell> echo "# Python 2.7.x" > requirements.txt
shell> echo "Django==1.11.1" >> requirements.txt

shell> pwd
~/class101/project

shell> ls -a
.  .. manage.py project requirements.txt

shell> pwd
~/class101/project

shell> ls -a project/
.  ..  __init__.py  settings.py  urls.py  wsgi.py

# Set project/settings.py ALLOWED_HOST = ['*']

shell> pwd
~/class101/project

shell> python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

Django version 1.11.1, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/

# Log into to your server from elsewhere with ssh -x -C -L 8000:127.0.0.1:8000
# and then request from browser http://127.0.0.1:8000
# Alternative, edit project/project/settings and set ALLOWED_HOST = ['*']
# request from browser http://fqdn:8000


# It there is no need to start over, then start here:
# Starting Week #2
shell> pwd
~/class101/project

shell> django-admin startapp dashboard

shell> ls dashboard/
admin.py  apps.py  __init__.py  migrations  models.py  tests.py  views.py

# Edit dashboard/models.py so it looks like this
shell> cat dashboard/models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Server(models.Model):
    '''https://docs.djangoproject.com/en/1.11/ref/models/fields/#genericipaddressfield '''
    name = models.CharField(max_length=200, unique=True)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)

    def __str__(self):
        return '{}:{}'.format(self.name, self.ip)

shell> pwd
~/class101/project

# Edit project/settings.py, adding 'dashboard' to the INSTALLED_APP variable.
# It will look like this

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'dashboard',
    ]

shell> pwd
~/class101/project

shell> python manage.py makemigrations
shell> python manage.py migrate

# Create 3 superusers - use fake data
shell> python manage.py createsuperuser
shell> python manage.py createsuperuser
shell> python manage.py createsuperuser

# What all happened?
# Let's look at the database

shell> pwd
~/class101/project

shell> python manage.py dbshell
sqlite> .tables
auth_group                  dashboard_server
auth_group_permissions      django_admin_log
auth_permission             django_content_type
auth_user                   django_migrations
auth_user_groups            django_session
auth_user_user_permissions

sqlite> .head on
sqlite> select * from auth_user;

id|password|last_login|is_superuser|first_name|last_name|email|is_staff|is_active|date_joined|username
1|pbkdf2_sha256$36000$2IApYcQq2GqG$rX3vbl1yLxSFon43geHDwleXNV+/x/kQ+sxoGVX9YgI=||1|||e@m.com|1|1|2017-05-14 23:54:18.054926|boo
2|pbkdf2_sha256$36000$QPND8w381guD$5TuzlZkCVVOMcWq/6dA8vkGp2Bntq1Q/Jv/GaviZ9ms=||1|||b@m.com|1|1|2017-05-14 23:54:39.241113|who
3|pbkdf2_sha256$36000$jmW5uR9z4M7h$RbE7XjX8vx3KYzgJ/u47sMWclzagEdS53XZAd5QO15s=||1|||c@d.com|1|1|2017-05-14 23:55:04.083796|moo

sqlite> .exit
```

### Week #3

```
shell> pwd
~/class101/project

shell> cat dashboard/admin.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Server

class ServerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Server, ServerAdmin)

shell> python manage.py runserver

# Browse to /admin
# Add some data for the dashboard app, server names and ips - use fake data
# Test the error checking on the form: can you add a garbage ip, do you get an error?
# does it check for uniqueness?

# Other cool stuff
shell> pwd
~/class101/project

shell> python manage.py shell
>>> from django.contrib.auth.models import User as U
>>> u = U.objects.all()
>>> for ea in u:
...     ea.email
...     print('Email: {}'.format(ea.email))
...
     u'a@b.com'
     Email: a@b.com
>>>
>>> from dashboard.models import Server
>>>
>>> s = Server.objects.all()
>>> for ea in s:
>>>     print('{}:{}'.format(ea.name, ea.ip))
...
>>>

# Let's work on the view
# Make your  project/urls.py look like this
shell> pwd
~/class101/project

shell> cat project/urls.py
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^admin/', admin.site.urls),
]


# Make the template directory
shell> pwd
~/class101/project

shell> mkdir -p dashboard/templates/dashboard

# Make sure your dashboard urls looks like this
shell> cat dashboard/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^server-list/$', views.server_list, name='server_list'),
]

# Extra - add servers on the command line
>>> from dashboard.models import Server
>>> s = Server()
>>> s.name = 'boo'
>>> s.ip = '192.168.2.1'
>>> s.save()
>>> 
>>> s = Server()
>>> s.name = 'boo'
>>> s.ip = '192.168.2.1'
>>> s.full_clean()
Traceback (most recent call last):
ValidationError: {'ip': [u'Server with this Ip already exists.'], 'name': [u'Server with this Name already exists.']}

>>> s.ip = '192'
>>> s.clean_fields()
Traceback (most recent call last):
ValidationError: {'ip': [u'Enter a valid IPv4 address.']}

>>>
>>> Server.objects.all()
>>>
>>> for ea in Server.objects.all():
...     print(ea)
...
boo:192.168.2.2
wow:192.168.1.1

# Make sure your dashboard/views.py looks like this
shell> pwd
~/class101/project


shell> cat dashboard/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Server


def server_list(request):
    servers = Server.objects.all()
    template = loader.get_template('dashboard/server_list.html')

    return HttpResponse(template.render(
        {'server_list': servers}, request
    ))

# Make sure your template looks like this
shell> cat dashboard/templates/dashboard/server_list.html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Server List</title>
    </head>
    <body>
        {% for ea in server_list %}
            <p>Server: {{ ea.name }}</p>
            <p>IP: {{ ea.ip }}</p>
        {% endfor %}
    </body>
</html>

# Get ready to browse to http://127.0.0.1:8000/dashboard/server-list/
shell> pwd
~/class101/project

shell> python manage.py runserver

```

###  Week #5 - Openshift

#### If you simply want to use johnedstone's class101 project, download these templates and skip to below where it says "Start openshift project": `oc login ... `

```
# Set up directory for templates
shell> pwd
~/class101/project

shell> mkdir -p openshift/templates

shell> curl -k -x <proxyip:port>  https://raw.githubusercontent.com/johnedstone/class101/master/project/openshift/templates/class101.yaml > openshift/templates/class101.yaml
shell> curl -k -x <proxyip:port>  https://raw.githubusercontent.com/johnedstone/class101/master/project/openshift/templates/class101_postgresql.yaml > openshift/templates/class101_postgresql.yaml

```

#### If you want to update your project so it will run in Openshift, follow these instructions here.

* Update the above templates with your git http repo url

* Make sure you move wsgi.py up one directory

```
shell> pwd
~/class101/project

shell> mv project/wsgi.py .

```

* Make sure your settings file knows that you've moved wsgi.py up one directory

```
# change project/settings.py, this one variable to look like this
shell> egrep wsgi project/settings.py
WSGI_APPLICATION = 'wsgi.application'

```

* Fix health/liveliness probe for Openshift

```
# Your urls.py file should look like this
shell> cat project/urls.py
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^$', lambda request:HttpResponse(status=200)),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^admin/', admin.site.urls),
]

```


* Add gunicorn,psycopg2, and whitenoise to requirements.txt for production

```
shell> pwd
shell> ~/class101/project
shell> cp requirements.txt requirements_local.txt

shell> echo gunicorn >> requirements.txt
shell> echo psycopg2 >> requirements.txt
shell> echo whitenoise >> requirements.txt

```

* Update project/settings.py, adding whitenoise

```
# add this whitenoise line right below the SecurityMiddleware line

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ....
        
```
* Update project/settings.py to allow for databases other than sqlite

```
# Remove these lines
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Add these lines
from . import database

DATABASES = {
    'default': database.config()
}

# add the file database.py in the same dir as settings.py
shell> cat project/database.py
import os

from django.conf import settings


engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
}


def config():
    service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    if service_name:
        engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['sqlite'])
    else:
        engine = engines['sqlite']
    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name)),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name)),
    }

# vim: ai et ts=4 sts=4 sw=4 nu ru

shell> pwd
~/class101/project
shell> tree -I "pyc"
.
|-- dashboard
|   |-- admin.py
|   |-- apps.py
|   |-- __init__.py
|   |-- migrations
|   |   |-- 0001_initial.py
|   |   `-- __init__.py
|   |-- models.py
|   |-- templates
|   |   `-- dashboard
|   |       `-- server_list.html
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- db.sqlite3
|-- manage.py
|-- openshift
|   `-- templates
|       |-- class101.yaml
|       `-- promotion_restapi_postgresql.yaml
|-- project
|   |-- database.py
|   |-- __init__.py
|   |-- settings.py
|   `-- urls.py
|-- requirements.txt
`-- wsgi.py

```

* git add, commit and push

```
shell> git add openshift project/database.py
shell> git commit -am "files for openhsift updated"
shell> git push
```

#### Start openshift project, app, etc.

```
shell> oc login https://fqdn:8443 -u youruserid
shell> oc new-project youruserid-class101
shell> export PIP_PROXY=<ip:port>; oc new-app --param=PIP_PROXY=${PIP_PROXY} -f openshift/templates/class101.yaml

# Note errors
shell> oc delete all --all
# Start again with
shell> oc new-app ....

shell> oc get pods
shell> oc logs -f bc/class101

shell> oc get pods -w
NAME                READY     STATUS              RESTARTS   AGE
class101-1-3k1ec    0/1       ContainerCreating   0          3s
class101-1-build    0/1       Completed           0          2m
class101-1-deploy   1/1       Running             0          13s

NAME               READY     STATUS    RESTARTS   AGE
class101-1-3k1ec   0/1       Running   0          8s

class101-1-3k1ec   1/1       Running   0         21s

class101-1-deploy   0/1       Completed   0         33s
class101-1-deploy   0/1       Terminating   0         33s
class101-1-deploy   0/1       Terminating   0         33s


^Cshell>

shell> oc get pods
NAME               READY     STATUS      RESTARTS   AGE
class101-1-3k1ec   1/1       Running     0          9m
class101-1-build   0/1       Completed   0          12m

shell> oc rsh class101-1-3k1ec
(app-root)sh-4.2$
(app-root)sh-4.2$ python manage.py createsuperuser --username=boohoo --email=a@b.com
Password:
Password (again):
Superuser created successfully.
exit

shell> oc get routes
NAME       HOST/PORT                                         PATH      SERVICES   PORT      TERMINATION
class101   class101-youruserid-class101.fqdn             class101   <all>

# Open your browser and navigate to the above /admin and add some IPs
# Navigate then to /dashboard/server-list/

```

* If you use the postgresql template your pods will look like this
```
shell> oc get pods
NAME                 READY     STATUS      RESTARTS   AGE
class101-1-0hoo2     1/1       Running     0          4m
class101-1-build     0/1       Completed   0          6m
postgresql-1-9f7dj   1/1       Running     0          6m
```

* When you are all done, delete your project.  Thank you!
```
# show your projectname
shell> oc project
shell> oc delete project <your project name>
``
```


* Instructions from Chris will go here

```
shell> 
```

###### vim: ai et ts=4 sts=4 sw=4 nu ru
