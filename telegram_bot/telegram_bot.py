import telebot
from decouple import config

from constants import OutPutMessages
from word2vec import LanguageModelService


class BotConfiguration:
    def __init__(self, language_model_service=None):
        self.bot_token = config('TELEGRAM_BOT_API_TOKEN')
        self.bot = telebot.TeleBot(self.bot_token)
        self.language_model_service: LanguageModelService = language_model_service

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message)

        @self.bot.message_handler(commands=['about_us'])
        def about_us_message(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)

        @self.bot.message_handler(content_types=['text'], chat_types=['supergroup', 'group'])
        def handle_group_text_message(message):
            chat_id = message.chat.id
            text = message.text

            token, sim_words = self.language_model_service.get_back_interesting_token_and_similar_words(text)
            if token:
                vote_message = OutPutMessages.which_one_has_the_closest_meaning(token)
                vote_options = [sim for sim in sim_words.keys()] + [OutPutMessages.none_of_the_above_options]
                self.bot.send_poll(chat_id, vote_message, vote_options, reply_to_message_id=message.id)

        def vote_done_condition(vote):
            # vote.options[0].text, vote.options[0].voter_count
            return vote.total_voter_count >= 1

        @self.bot.poll_handler(func=vote_done_condition)
        def handle_vote_submit(poll_answer):
            print(poll_answer)
            # self.bot.send_message(chat_id=chat_id, text=OutPutMessages.got_it)


if __name__ == '__main__':
    conf = BotConfiguration()
    print('running bot:')

    conf.bot.polling(none_stop=True, interval=10, timeout=1000)
