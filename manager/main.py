import logging
logging.basicConfig(filename='app.log', filemode='w',format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from telethon.sync import TelegramClient, events
import asyncio

from config import Config
import time

api_id = 429974
api_hash = 'ce871eefb9e04372705347d84431d3a4'

async def main():
   while True:
      await asyncio.sleep(10)
      await client.send_message(258273164, 'Ты залупа')

with TelegramClient('name', api_id, api_hash) as client:



   @client.on(events.NewMessage(incoming=True))
   async def handler(event):
      await event.reply('Ты пидор 😂')
   
   client.loop.create_task(main())

   client.run_until_disconnected()