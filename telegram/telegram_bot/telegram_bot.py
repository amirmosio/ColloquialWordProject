import asyncio
import os
import telebot.async_telebot as telebot
from decouple import config
# import telebot
from aiohttp import web
from http.server import BaseHTTPRequestHandler, HTTPServer
from word2vec import Word2VecLanguageModelService


class BotConfiguration:

    def __init__(self, language_model_service=None):
        self.bot_token = config('TELEGRAM_BOT_API_TOKEN')
        self.bot = telebot.AsyncTeleBot(self.bot_token)
        self.language_model_service: Word2VecLanguageModelService = language_model_service

        # self.WEBHOOK_HOST = '<ip/host where the bot is running>'
        # self.WEBHOOK_PORT = int(os.environ.get('PORT', 5000))
        # self.WEBHOOK_LISTEN = '0.0.0.0'
        #
        # self.WEBHOOK_URL_BASE = "https://%s:%s" % (self.WEBHOOK_HOST, self.WEBHOOK_PORT)
        # self.WEBHOOK_URL_PATH = "/%s/" % (self.bot_token)

    async def run_bot(self):
        # httpd = HTTPServer((conf.WEBHOOK_LISTEN, conf.WEBHOOK_PORT), conf.WebhookHandler)
        # httpd.serve_forever()

        await self.bot.polling(none_stop=True, interval=10)

    # async def handle(self, request):
    #     if request.match_info.get('token') == self.bot.token:
    #         request_body_dict = await request.json()
    #         update = telebot.types.Update.de_json(request_body_dict)
    #         await self.bot.process_new_updates([update])
    #         return web.Response()
    #     else:
    #         return web.Response(status=403)


if __name__ == '__main__':
    conf = BotConfiguration()
    asyncio.run(conf.run_bot())
