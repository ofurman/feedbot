import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    POSTGRESQL_DATABASE_URI="postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}".format(
        POSTGRES_USER=os.environ.get('POSTGRES_USER'),
        POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD'),
        POSTGRES_DB=os.environ.get('POSTGRES_DB')
    )

    API_ID = os.environ.get('API_ID')
    API_HASH = os.environ.get('API_HASH')
    BOT_ID = int(os.environ.get('BOT_ID'))