import telebot

from constants import OutPutMessages
from telegram.database_utility import SqliteQueryUtils
from telegram_bot import BotConfiguration


class ClientBotHandler:
    def __init__(self):
        self.database_utility: SqliteQueryUtils = SqliteQueryUtils()
        self.bot: BotConfiguration = BotConfiguration()
        self.my_client: MusicChannelForResearchClient = None

        @self.bot.bot.message_handler(commands=['start'])
        async def start_message(message):
            chat_id = message.chat.id
            channels = MusicChannelForResearchClient.telegram_music_channels
            markup = telebot.types.InlineKeyboardMarkup()
            for ch in channels:
                markup.add(telebot.types.InlineKeyboardButton(text=ch, callback_data=f'select_{ch}'))
            await self.bot.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message_with_channel(channels),
                                            reply_markup=markup)

        def select_channel_func_condition(call):
            c = call.data.startswith("select_")
            c = c and call.data[7:] in MusicChannelForResearchClient.telegram_music_channels
            return c

        @self.bot.bot.callback_query_handler(func=select_channel_func_condition)
        async def query(call):
            await self.bot.bot.edit_message_reply_markup(call.from_user.id, message_id=call.message.message_id,
                                                         reply_markup=None)
            selected_channel = call.data[7:]
            self.database_utility.change_user_channel(call.from_user.id, selected_channel)
            musics = await self.my_client.get_channel_all_music_counts(selected_channel)
            await self.bot.bot.edit_message_text(OutPutMessages.good_choice_music_condition(selected_channel, musics),
                                                 call.from_user.id, message_id=call.message.message_id)
            await self.bot.bot.unpin_all_chat_messages(call.from_user.id)
            await self.bot.bot.pin_chat_message(call.from_user.id, call.message.message_id)

        @self.bot.bot.message_handler(commands=['about_us'])
        async def about_us_message(message):
            chat_id = message.chat.id
            await self.bot.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)

        @self.bot.bot.message_handler(commands=['gimme'])
        async def gimme(message):
            chat_id = message.chat.id
            try:
                select_channel = self.database_utility.get_user_selected_channel(chat_id)
                music_message = await self.my_client.select_a_music_randomly_with_best_local_score(select_channel)
                forwarded_music = await self.my_client.send_client_message_to_my_bot(music_message)
                await self.bot.bot.forward_message(chat_id=chat_id, message_id=forwarded_music.id,
                                                   from_chat_id=forwarded_music.sender.id)
            except Exception as e:
                await self.bot.bot.send_message(chat_id=chat_id, text=OutPutMessages.select_one_of_channels)

        @self.bot.bot.message_handler(content_types=['text'], chat_types=['supergroup', 'group'])
        def handle_group_text_message(message):
            chat_id = message.chat.id
            text = message.text

            token, sim_words = self.bot.language_model_service.get_back_interesting_token_and_similar_words(text)
            if token:
                vote_message = OutPutMessages.which_one_has_the_closest_meaning(token)
                vote_options = [sim for sim in sim_words.keys()] + [OutPutMessages.none_of_the_above_options]
                self.bot.bot.send_poll(chat_id, vote_message, vote_options, reply_to_message_id=message.id)

        def vote_done_condition(vote):
            # vote.options[0].text, vote.options[0].voter_count
            return vote.total_voter_count >= 1

        @self.bot.bot.poll_handler(func=vote_done_condition)
        def handle_vote_submit(poll_answer):
            print(poll_answer)
            # self.bot.send_message(chat_id=chat_id, text=OutPutMessages.got_it)

        @self.bot.bot.message_handler()
        async def message_handler(message):
            print(message)

    async def start(self):
        async with MusicChannelForResearchClient() as my_client:
            print("Client bot connected")
            self.my_client = my_client

            await self.bot.bot.polling(none_stop=True, interval=10, timeout=1000)

    async def end(self):
        await self.my_client.__aexit__(None, None, None)
        await self.bot.bot.stop_polling()
