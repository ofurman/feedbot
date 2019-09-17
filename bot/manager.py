import asyncio
from collections import OrderedDict

#DTABASE
from db import open_session
from db.models import User, Channel

from telethon.tl.types import Message
from telethon.errors import RPCError, ChannelPrivateError

from config import Config.manager_client as client
from datetime import datetime, timedelta

class Manager():
    __slots__ = ['_queue', '_current_task']

    def __init__(self):
        self._queue = OrderedDict()
        self._current_task = None

    def add(self, channel: Channel):
        pass

    def remove(self, channel: Channel):
        pass

    async def start(self, _=None):
        async with open_session() as session:
            channels = session.query(Channel).all()
            for channel in channels:
                self._add_to_queue(channel)
        self._new_task()

    async def stop(self, _=None):
        if not self._current_task:
            return
        self._current_task.remove_done_callback(self._new_task)
        try:
            await asyncio.wait_for(self._current_task, timeout=1)
        except asyncio.TimeoutError:
            pass
        finally:
            for coro in self._queue.values():
                coro.close()
            self._queue.clear()
        self._current_task = None


    async def _get_messages(self, channel: Channel):
        msgs = []
        try:
            msgs = client.get_messages(entity=channel.link,
                                        limit=100,
                                        min_id=channel.last_id,
                                        wait_time=5,
                                        reverse=True)
        except ConnectionError:
            await asyncio.sleep(60)
        except RPCError as e:
            print(e)
        except ChannelPrivateError:
            print("channel is private")
            async with open_session() as session:
                session.delete(channel)
        return [m for m in msgs if isinstance(m, Message)]
        
    async def _forward_messages(self, channel: Channel):
        messages = self._get_messages(channel=channel)
        if messages:
            try:
                await client.forward_messages(ch.feed, msgs)
            except ConnectionError:
                await asyncio.sleep(60)
            except RPCError as e:
                print(e)
                await asyncio.sleep(60)
            else:
                async with open_session() as session:
                    channel.last_id = messages[-1].id
        return await asyncio.sleep(len(msgs) or 60, channel)

    def _add_to_queue(self, channel: Channel):
        self._queue[channel.link] = self._forward_messages(channel)

    def _new_task(self, future=None):
        if self._current_task:
            self._add_to_queue(future.resut())
        if self._queue:
            _, coro = self._queue.popitem(last=False)
            self._current_task = asyncio.create_task(coro)
            self._current_task.add_done_callback(self._new_task)



