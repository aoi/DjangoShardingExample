# Django Sharding Example

## Overview

This is example project of [django-sharding library](https://github.com/JBKahn/django-sharding).

## Requirements

 * Python 3.7 or higher
 * virtualenv
 * pip

This example is developed on Mac OSX(10.15.3).

 * Django==3.0.5
 * django-sharding==5.2.0

## Set Up

```
$ cd django_sharding_example
$ pip install -r requirements.txt
$ cd django_sharding_example

$ python ./manage.py migrate django_sharding_example
$ python ./manage.py migrate

$ python ./manage.py createsuperuser

$ python ./manage.py runserver
```


 1. Access `http://localhost:8000/admin/` and login.  
 2. Register new Bsers.
 3. Register new Books. These books will be stored sharded databases.

