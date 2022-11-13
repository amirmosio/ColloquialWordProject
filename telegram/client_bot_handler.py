from handlers.profile_handler import handler_profile
from handlers.question_handler import handler_question
from language_models import LanguageModelService
from services import SqliteQueryServices
from telegram_bot import BotConfiguration
from telegram_client import ResearchTelegramClient


class ClientBotHandler:
    def __init__(self):
        self.language_model_service = LanguageModelService()
        self.database_utility: SqliteQueryServices = SqliteQueryServices()
        self.telebotConf: BotConfiguration = None
        self.my_client: ResearchTelegramClient = None

    async def start(self):
        print("Client bot connected")
        self.my_client = ResearchTelegramClient(self.language_model_service)
        await self.my_client.run_bot()
        print("Telegram bot polling started")
        self.telebotConf = BotConfiguration()
        await self.telebotConf.run_bot()

        handler_profile(self)
        # handler_music(self)
        handler_question(self)

    async def end(self):
        await self.my_client.__aexit__(None, None, None)
        await self.telebotConf.bot.stop_polling()
