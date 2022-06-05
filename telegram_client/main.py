import datetime as dt
from datetime import datetime

from decouple import config
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterMusic

phone_number = config('TELEGRAM_CLIENT_PHONE_NUMBER')
api_id = config('TELEGRAM_CLIENT_API_ID')
api_hash = config('TELEGRAM_CLIENT_API_HASH')


class MusicChannelForResearchClient:
    telegram_music_channels = ["https://t.me/sharethejoy", "https://t.me/RadioRelax"]

    def __init__(self):
        self.client = TelegramClient("my research client", api_id, api_hash)

    def __enter__(self):
        self.client.connect()
        is_authorized = self.client.is_user_authorized()
        if not is_authorized:
            self.client.send_code_request(phone_number)
            self.client.sign_in(phone_number, input('Enter the code: '))
        return self

    def get_music_channel_subscription_number(self, channel_name):
        channel_full_info = self.get_channel_full_info(channel_name)
        return channel_full_info.full_chat.participants_count

    def get_channel_full_info(self, channel_name):
        channel_connect = self.client.get_entity(channel_name)
        channel_full_info = self.client(GetFullChannelRequest(channel_connect))
        return channel_full_info

    def get_channel_create_date(self, channel_name):
        channel_connect = self.client.get_entity(channel_name)
        for message in self.client.iter_messages(channel_connect, reverse=True, filter=InputMessagesFilterMusic,
                                                 limit=1, add_offset=0):
            return message.date

    def get_channel_music_messages(self, channel_name, limit=100, reverse=True, add_offset=0):
        channel_connect = self.client.get_entity(channel_name)
        messages = self.client.get_messages(channel_connect, limit=limit, filter=InputMessagesFilterMusic,
                                            reverse=reverse, add_offset=add_offset)
        return messages

    def get_channel_all_music_counts(self, channel_name):
        channel_connect = self.client.get_entity(channel_name)
        musics = self.client(SearchRequest(
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
        replies = getattr(message_object.replies, "replies", 0)
        message_views = message_object.views
        message_create_date = message_object.date
        message_passed_days = (datetime.now(tz=dt.timezone.utc) - message_create_date).days
        channel_days = (datetime.now(tz=dt.timezone.utc) - channel_first_message_date).days
        participants_coeff = ((channel_days - message_passed_days) / channel_days)
        old_channel_participants = int(channel_object.full_chat.participants_count * max(participants_coeff, 0.001))
        past_view_ratio = message_views / old_channel_participants
        return past_view_ratio * (replies + 1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()
        return False


if __name__ == '__main__':
    with MusicChannelForResearchClient() as my_client:
        channel_name = MusicChannelForResearchClient.telegram_music_channels[0]
        res = my_client.get_music_channel_subscription_number(channel_name)
        print(res)
        messages = my_client.get_channel_music_messages(channel_name)
        channel_create_date = my_client.get_channel_create_date(channel_name)
        channel_full_info = my_client.get_channel_full_info(channel_name)
        for message in messages:
            print(str(message.message), str(message.audio.id), message.views, message.id)
            res = my_client.get_music_score(channel_full_info, channel_create_date, message)
            print(res)

        #############
        res = my_client.get_channel_all_music_counts(channel_name)
        print(f"music counts: {res}")
