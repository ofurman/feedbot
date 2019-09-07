#DATABASE
from config import Config

from db import Session, Base, engine
from db.models import User, Channel

from contextlib import asynccontextmanager

import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook


API_TOKEN = os.environ.get('TG_API_KEY')
MANAGER_ID = os.environ.get('MANAGER_ID')
ADMIN_ID = os.environ.get('ADMIN_ID')

#Load database
Base.metadata.create_all(engine)

@asynccontextmanager
async def open_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()

# webhook settings
WEBHOOK_HOST = os.environ.get('URL_HOSTNAME')
WEBHOOK_PATH = os.environ.get('URL_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 5001

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    #TODO: Write start message
    async with open_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user is None:
            user = User(id=message.from_user.id, username=message.from_user.username, 
                                language_code=message.from_user.language_code)
            session.add(user)
        await bot.send_message(message.chat.id, user)

@dp.message_handler(commands=['mychannels'])
async def list_my_channels(message: types.Message):
    async with open_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user is None:
            user = User(id=message.from_user.id, username=message.from_user.username, 
                                language_code=message.from_user.language_code)
            session.add(user)
        reply_msg = 'Вы подписаны на:\n'
        for channel in user.channels:
            reply_msg += '➡️ {}\n'.format(channel.title)
        await bot.send_message(message.chat.id, reply_msg)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    #TODO: Write help message
    return SendMessage(message.chat.id, message.text)

@dp.message_handler(lambda message: (message.forward_from_chat.type == 'channel') and (str(message.from_user.id) != MANAGER_ID))
async def subscribe(message: types.Message):
    async with open_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user is None:
            user = User(id=message.from_user.id, username=message.from_user.username, 
                                language_code=message.from_user.language_code)
            session.add(user)
        
        channel = session.query(Channel).filter_by(id=str(message.forward_from_chat.id)).first()
        if channel is None:
            channel = Channel(id=message.forward_from_chat.id, 
                                title=message.forward_from_chat.title,
                                username=message.forward_from_chat.username)

        user.channels.append(channel)
        await bot.send_message(user.id, "Вы подписались на канал [{}](@{})".format(channel.title, channel.username), parse_mode=types.ParseMode.MARKDOWN)



@dp.message_handler(lambda message: (message.forward_from_chat.type == 'channel') and (str(message.from_user.id) == MANAGER_ID))
async def broadcast(message: types.Message):
    async with open_session() as session:
        channel = session.query(Channel).filter_by(id=str(message.forward_from_chat.id)).first()
        for user in channel.subs:
            await message.forward(user.id)




async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    session.close()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
