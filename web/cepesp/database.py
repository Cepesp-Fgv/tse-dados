from peewee import MySQLDatabase, Model, TextField, CharField, DateTimeField, AutoField

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
    last_status = CharField()
    athena_id = CharField()
    created_at = DateTimeField()


def migrate():
    open_connection()
    database_client.create_tables([CacheEntry])
    close_connection()


def open_connection():
    try:
        database_client.connect(reuse_if_open=True)
    except Exception as e:
        print(e)
        pass


def close_connection():
    try:
        database_client.close()
    except Exception as e:
        print(e)
        pass
