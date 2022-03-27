import telebot

from constants import OutPutMessages


class BotConfiguration:
    def __init__(self):
        self.bot_token = BotConfiguration.load_bot_token()
        self.bot = telebot.TeleBot(self.bot_token)

    @classmethod
    def load_bot_token(cls):
        from decouple import config
        return config('TELEGRAM_BOT_API_TOKEN')


conf = BotConfiguration()


@conf.bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message)


@conf.bot.message_handler(commands=['about_us'])
def about_us_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)


@conf.bot.message_handler(content_types=['text'], chat_types=['supergroup', 'group'])
def handle_group_text_message(message):
    chat_id = message.chat.id
    message_id = message.id
    print(message.text)
    # conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.got_it)
    conf.bot.send_poll(chat_id, message.text, ['hello1', 'hello2'], reply_to_message_id=message_id)


def func(a):
    # TODO
    return a.total_voter_count >= 1


@conf.bot.poll_handler(func=func)
def handle_vote_submit(poll_answer):
    print(poll_answer)
    # conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.got_it)



