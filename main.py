from language_model.word2vec import LanguageModelService
from telegram_bot import BotConfiguration

if __name__ == '__main__':
    language_model_service = LanguageModelService()

    conf = BotConfiguration(language_model_service)
    print('running bot:')

    conf.bot.polling(none_stop=True, interval=10, timeout=1000)

