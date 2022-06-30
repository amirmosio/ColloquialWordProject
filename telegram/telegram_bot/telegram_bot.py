import asyncio

import telebot.async_telebot as telebot
from decouple import config

from word2vec import LanguageModelService


class BotConfiguration:
    def __init__(self, language_model_service=None):
        self.bot_token = config('TELEGRAM_BOT_API_TOKEN')
        self.bot = telebot.AsyncTeleBot(self.bot_token)
        self.language_model_service: LanguageModelService = language_model_service


if __name__ == '__main__':
    async def run_bot():
        conf = BotConfiguration()
        print('running bot:')

        await conf.bot.polling(none_stop=True, interval=10, timeout=1000)


    asyncio.run(run_bot())
