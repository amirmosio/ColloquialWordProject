from handlers.music_handler import handler_music
from handlers.profile_handler import handler_profile
from handlers.question_handler import handler_question
from services import SqliteQueryServices
from telegram_bot import BotConfiguration
from telegram_client import MusicChannelForResearchClient


class ClientBotHandler:
    def __init__(self):
        self.database_utility: SqliteQueryServices = SqliteQueryServices()
        self.telebotConf: BotConfiguration = BotConfiguration()
        self.my_client: MusicChannelForResearchClient = None

        handler_profile(self)
        handler_music(self)
        handler_question(self)
    # @client_bot_handler.telebotConf.bot.message_handler(commands=['about_us'])
    # async def about_us_message(message):
    #     chat_id = message.chat.id
    #     await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)
    async def start(self):
        async with MusicChannelForResearchClient() as my_client:
            print("Client bot connected")
            self.my_client = my_client

            await self.telebotConf.bot.polling(none_stop=True, interval=10, timeout=1000)

    async def end(self):
        await self.my_client.__aexit__(None, None, None)
        await self.telebotConf.bot.stop_polling()
