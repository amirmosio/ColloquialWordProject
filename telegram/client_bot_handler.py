from handlers.profile_handler import handler_profile
from handlers.question_handler import handler_question
from language_models import LanguageModelService
from services import SqliteQueryServices
from telegram_bot import BotConfiguration
from telegram_client import MusicChannelForResearchClient


class ClientBotHandler:
    def __init__(self):
        self.language_model_service = LanguageModelService()
        self.database_utility: SqliteQueryServices = SqliteQueryServices()
        self.telebotConf: BotConfiguration = BotConfiguration()
        self.my_client: MusicChannelForResearchClient = None

        handler_profile(self)
        # handler_music(self)
        handler_question(self)

    async def start(self):
        async with MusicChannelForResearchClient(self.language_model_service) as my_client:
            print("Client bot connected")
            self.my_client = my_client
            print("Telegram bot polling started")
            await self.telebotConf.bot.polling(none_stop=True, interval=10, timeout=1000)

    async def end(self):
        await self.my_client.__aexit__(None, None, None)
        await self.telebotConf.bot.stop_polling()
