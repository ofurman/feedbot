#DATABASE
import config

import db
from db import open_session
from db.models import User, Channel
import db.events

import logging
import os

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

#FSM IMPORT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import manager_client as client


API_TOKEN = os.environ.get('TG_API_KEY')
MANAGER_ID = os.environ.get('MANAGER_ID')
ADMIN_ID = os.environ.get('ADMIN_ID')

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

############################################################################################################
###### COMMAND HANDLERS
############################################################################################################

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
    reply_msg = 'HELP MESSAGE'
    bot.send_message(message.chat.id, reply_msg)

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    async with open_session() as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user is None:
            user = User(id=message.from_user.id, username=message.from_user.username, 
                                language_code=message.from_user.language_code)
            session.add(user)

        for channel in user.channels:
            inline_kb = types.InlineKeyboardMarkup(row_width=1)
            button = types.InlineKeyboardButton('❌ Отписаться', callback_data='unsubscribe{}'.format(channel.id))
            inline_kb.insert(button)
            await bot.send_message(message.chat.id, channel.title, reply_markup=inline_kb)
        

@dp.callback_query_handler(lambda c: 'unsubscribe' in c.data)
async def process_unsubscribe_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    async with open_session() as session:
        channel_id = callback_query.data.strip('unsubscribe')

        user = session.query(User).filter_by(id=callback_query.from_user.id).first()
        if user is None:
            user = User(id=callback_query.from_user.id, username=callback_query.from_user.username, 
                                language_code=callback_query.from_user.language_code)
            session.add(user)
        try:
            channel = session.query(Channel).filter_by(id=channel_id).first()
            user.channels.remove(channel)
            print(channel.subs, flush=True)
            session.delete(channel)
        except Exception as e:
            reply_msg = f'🆘Усп, произошла ошибка.\nВы не подписаны на этот канал 😟\n\nЕсли функционал работает неправильно, напишите @lesha_f\n{e}'
            await bot.send_message(callback_query.from_user.id, reply_msg)
        else:
            reply_msg = '✅Вы успешно отписались от {}'.format(channel.title)
            await bot.send_message(callback_query.from_user.id, reply_msg)


############################################################################################################
###### END COMMAND HANDLERS
############################################################################################################

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



# @dp.message_handler(lambda message: (str(message.from_user.id) == MANAGER_ID))
# async def broadcast(message: types.Message):
#     async with open_session() as session:
#         channel = session.query(Channel).filter_by(id=str(message.forward_from_chat.id)).first()
#         print(channels.subs)
#         for user in channel.subs:
#             await message.forward(user.id)







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
    with client:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
