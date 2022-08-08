import asyncio

from client_bot_handler import ClientBotHandler

if __name__ == '__main__':
    handler = ClientBotHandler()
    asyncio.run(handler.start())
