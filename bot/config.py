import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRESQL_DATABASE_URI="postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}".format(
        POSTGRES_USER=os.environ.get('POSTGRES_USER'),
        POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD'),
        POSTGRES_DB=os.environ.get('POSTGRES_DB')
    )

    BOT_API_TOKEN = os.environ.get('TG_API_KEY')
    BOT_WEBHOOK_HOST = os.environ.get('URL_HOSTNAME')