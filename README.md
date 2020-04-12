# Django Sharding Example

## Overview

This is example project of [django-sharding library](https://github.com/JBKahn/django-sharding).

 * Default DB
    * User
    * ShardedBookID
 * Sharded DB
    * ShardedUser
        * This models is for foreign key from Book's user_id. We have User table, so this table seems unnecessary. But if this table's user_id is deleted, other tables data which is belong to this user_id will be deleted automaticaly by foreign key. It is convinient.
    * Book
        * This model is belong to User indirectly by foreign key to ShardedUser. Because Django can't use foreign key between multiple databases.

```
User.id = ShardedUser.user_id = Book.user
```

## Requirements

 * Python 3.7 or higher
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
 2. Register new Users. Then ShardedUser will be stored insharded databases which is specified User.shard.
 3. Register new Books. These books will be stored in sharded databases.
