from django.db import models
from django.contrib.auth.models import AbstractUser
from django_sharding_library.fields import ShardForeignKeyStorageField, TableShardedIDField
from django_sharding_library.models import ShardedByMixin, ShardStorageModel, TableStrategyModel
from django_sharding_library.decorators import model_config, shard_storage_config

# Models for not sharded database(default)
@shard_storage_config()
class User(AbstractUser, ShardedByMixin):
    pass

@model_config(database='default')
class ShardedBookID(TableStrategyModel):
    """
        ID for Book.
    """
    pass

# Models for sharded database
@model_config(shard_group='default')
class ShardedUser(models.Model):
    """
        This table has user_id.
        This user_id is supposed to be stored same shard db as user.shard in default db.
    """
    id = TableShardedIDField(primary_key=True, source_table_name='django_sharding_example.ShardedBookID')
    user_id = models.PositiveIntegerField()

    def get_shard(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.get(pk=self.user_id).shard


@model_config(shard_group='default')
class Book(models.Model):
    id = TableShardedIDField(primary_key=True, source_table_name='django_sharding_example.ShardedBookID')
    user = models.ForeignKey(ShardedUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    def __str__(self):
        return 'Book ({})'.format(self.title)

    def get_shard(self):
        return self.user.shard
