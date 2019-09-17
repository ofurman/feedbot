import os
from telethon.sync import TelegramClient
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRESQL_DATABASE_URI="postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}".format(
    POSTGRES_USER=os.environ.get('POSTGRES_USER'),
    POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD'),
    POSTGRES_DB=os.environ.get('POSTGRES_DB')
)

BOT_API_TOKEN = os.environ.get('TG_API_KEY')
BOT_WEBHOOK_HOST = os.environ.get('URL_HOSTNAME')

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_ID = int(os.environ.get('BOT_ID'))

manager_client = TelegramClient('/usr/src/manager/session/manager', API_ID, API_HASH)