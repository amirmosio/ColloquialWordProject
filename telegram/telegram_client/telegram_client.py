import asyncio
import datetime as dt
import math
import random
from datetime import datetime

import cachetools.func
from decouple import config
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterMusic

from CommandHandler import ColloquialCommandHandler

phone_number = config('TELEGRAM_CLIENT_PHONE_NUMBER')
api_id = config('TELEGRAM_CLIENT_API_ID')
api_hash = config('TELEGRAM_CLIENT_API_HASH')


class MusicChannelForResearchClient:
    telegram_music_channels = ["sharethejoy", "RadioRelax", "bikalammusic", "vmusicir"]

    def __init__(self):
        self.client = TelegramClient("my research client", api_id, api_hash)

    async def __aenter__(self):
        await self.client.connect()
        is_authorized = await self.client.is_user_authorized()
        if not is_authorized:
            await self.client.send_code_request(phone_number)
            await self.client.sign_in(phone_number, input('Enter the code: '))

        return self

    @cachetools.func.ttl_cache(maxsize=None, ttl=60 * 60 * 24)
    async def get_music_channel_subscription_number(self, channel_name):
        channel_full_info = await self.get_channel_full_info(channel_name)
        return channel_full_info.full_chat.participants_count

    async def get_channel_full_info(self, channel_name):
        channel_connect = await self.client.get_entity(channel_name)
        channel_full_info = await self.client(GetFullChannelRequest(channel_connect))
        return channel_full_info

    async def get_channel_create_date(self, channel_name):
        channel_connect = await self.client.get_entity(channel_name)
        async for message in self.client.iter_messages(channel_connect, reverse=True, filter=InputMessagesFilterMusic,
                                                       limit=1, add_offset=0):
            return message.date

    async def get_channel_music_messages(self, channel_name, limit=100, reverse=True, add_offset=0, min_id=0,
                                         max_id=math.inf):
        channel_connect = await self.client.get_entity(channel_name)
        messages = await self.client.get_messages(channel_connect, limit=limit, filter=InputMessagesFilterMusic,
                                                  reverse=reverse, add_offset=add_offset, min_id=min_id, max_id=max_id)
        return messages

    async def get_channel_all_music_counts(self, channel_name):
        channel_connect = await self.client.get_entity(channel_name)
        musics = await self.client(SearchRequest(
            channel_connect,  # peer
            '',  # q
            InputMessagesFilterMusic(),  # filter
            None,  # min_date
            None,  # max_date
            0,  # offset_id
            0,  # add_offset
            0,  # limit
            0,  # max_id
            0,  # min_id
            0  # hash
        ))
        return musics.count

    def get_music_score(self, channel_object, channel_first_message_date, message_object):
        replies = getattr(message_object.replies, "replies", 0) * 0.2
        message_views = message_object.views
        message_create_date = message_object.date
        message_passed_days = (datetime.now(tz=dt.timezone.utc) - message_create_date).days
        channel_days = (datetime.now(tz=dt.timezone.utc) - channel_first_message_date).days
        participants_coeff = ((channel_days - message_passed_days) / channel_days)
        old_channel_participants = int(channel_object.full_chat.participants_count * max(participants_coeff, 0.001))
        past_view_ratio = message_views / old_channel_participants
        return past_view_ratio * (replies + 1)

    async def select_a_music_randomly_with_best_local_score(self, channel_name):
        channel_connect = await self.client.get_entity(channel_name)
        last_music_id = None
        async for message in self.client.iter_messages(channel_connect, reverse=False, filter=InputMessagesFilterMusic,
                                                       limit=1, add_offset=0):
            last_music_id = message.id
            break
        random_id = random.choice(list(range(last_music_id - 60)))
        messages = await self.get_channel_music_messages(channel_name, limit=20, min_id=random_id)
        channel_full_info = await self.get_channel_full_info(channel_name)
        channel_create_date = await self.get_channel_create_date(channel_name)
        musics_score_tuples = [(self.get_music_score(channel_full_info, channel_create_date, message), message) for
                               message in messages]
        musics_score_tuples.sort()
        return musics_score_tuples[-1][1]

    async def send_client_message_to_my_bot(self, message):
        bot_username = "fa_cwc_bot"
        entity = await self.client.get_entity(bot_username)
        return await self.client.forward_messages(entity, message)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()
        return False


async def test():
    print("running client")

    async with MusicChannelForResearchClient() as my_client:
        channel_name = MusicChannelForResearchClient.telegram_music_channels[0]
        res = await my_client.get_music_channel_subscription_number(channel_name)
        print(res)
        messages = await my_client.get_channel_music_messages(channel_name)
        channel_create_date = await my_client.get_channel_create_date(channel_name)
        channel_full_info = await my_client.get_channel_full_info(channel_name)
        for message in messages:
            print(str(message.message), str(message.audio.id), message.views, message.id)
            res = my_client.get_music_score(channel_full_info, channel_create_date, message)
            print(res)

        #############
        res = await my_client.get_channel_all_music_counts(channel_name)
        print(f"music counts: {res}")

        ColloquialCommandHandler(my_client)
        await my_client.client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(test())
