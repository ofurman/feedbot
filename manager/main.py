import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger('feedmanager')

from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

from telethon.tl.types import PeerChannel


#DTABASE
from db import Session, Base, engine
from db.models import User, Channel

from config import Config
from datetime import datetime, timedelta

from contextlib import asynccontextmanager

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

api_id = Config.API_ID
api_hash = Config.API_HASH
DELAY = 1
BIG_DELAY = 60

with TelegramClient('/usr/src/manager/session/manager', api_id, api_hash) as client:
   async def main():
      async with open_session() as session:
         while True:
            timestamp = datetime.utcnow()
            await asyncio.sleep(BIG_DELAY)
            channels = session.query(Channel).all()
            for channel in channels:
               await asyncio.sleep(DELAY)
               channel_username = channel.username # your channel
               channel_entity= await client.get_entity(channel_username)
               async for message in client.iter_messages(entity=channel_entity, limit=10,
                                                         offset_date=timestamp, reverse=True):
                  logger.info('{}\t{}\n -- {}\n'.format(channel.username,message.date, message.text))
                  await message.forward_to(Config.BOT_ID)

   @client.on(events.NewMessage(outgoing=True, pattern=r'\.delay'))
   async def set_delay(event):
      try:
         DELAY = int(event.raw_text().strip('.delay '))
      except ValueError:
         await event.reply('ValueError occured. Please ceck parameter value')
      except:
         await event.reply('Error occured. Please ceck parameter value')
      else:
         await event.reply('DELAY was set to {}'.format(DELAY))
   
   @client.on(events.NewMessage(outgoing=True, pattern=r'\.bigdelay'))
   async def set_delay(event):
      try:
         BIG_DELAY = int(event.raw_text().strip('.bigdelay '))
      except ValueError:
         await event.reply('ValueError occured. Please ceck parameter value')
      except:
         except:
         await event.reply('Error occured. Please ceck parameter value')
      else:
         await event.reply('BIG_DELAY was set to {}'.format(BIG_DELAY))
   
   client.loop.create_task(main())

   client.run_until_disconnected()