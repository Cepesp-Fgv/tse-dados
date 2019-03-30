from peewee import MySQLDatabase, Model, TextField, CharField, DateTimeField, AutoField, SQL

from web.cepesp.config import DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT

database_client = MySQLDatabase(DB_DATABASE, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)


class BaseModel(Model):
    class Meta:
        database = database_client


class CacheEntry(BaseModel):
    class Meta:
        table_name = 'cache_entries'

    id = AutoField()
    sql = TextField()
    name = CharField()
    env = CharField()
    athena_id = CharField()
    created_at = DateTimeField()


def migrate():
    database_client.create_tables([CacheEntry])
