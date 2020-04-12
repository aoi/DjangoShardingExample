import dataclasses
from django.conf import settings
from django.db import models
from django.contrib import admin
from django_sharding_library.utils import get_possible_databases_for_model
from .models import User, ShardedUser, Book

def get_shards(model):
    """
        Get shards(only primary db).
    """
    shards = []
    for s in get_possible_databases_for_model(model):
        db_config = settings.DATABASES[s]
        if db_config.get('PRIMARY') is None:
            shards.append(s)

    return shards

class UserAdmin(admin.ModelAdmin):

    # If User is stored, ShardedUser will be stored to shard db which is specified by this user.shard
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Save to shard database also
        ShardedUser(user_id = obj.id).save()

class BookAdmin(admin.ModelAdmin):

    # Following methods limit to access default db.
    # https://docs.djangoproject.com/en/3.0/topics/db/multi-db/#exposing-multiple-databases-in-django-s-admin-interface
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.model.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.model.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        return super().formfield_for_manytomany(db_field, request, using=self.model.using, **kwargs)


admin.site.register(User, UserAdmin)

# register Book with dynamic Model
# admin.site.register() can't register same model.
# https://dynamic-models.readthedocs.io/en/latest/
shards = get_shards(Book)
for shard in shards:
    name = 'Books ({})'.format(shard)
    BookProxy = type('BookProxy_{}'.format(shard), (Book, ), {'__module__': 'django_sharding_example.models', 'Meta': type('Meta', (object,), {'proxy': True, 'verbose_name': name, 'verbose_name_plural': name}), 'using': shard})

    admin.site.register(BookProxy, BookAdmin)