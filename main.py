from gensim.models import Word2Vec


def get_language_model():
    return Word2Vec.load("language_model/word2vec.model")


def run_bot():
    from telegram_bot import conf
    print('running bot:')

    conf.bot.polling(none_stop=True, interval=10, timeout=1000)


if __name__ == '__main__':
    model = get_language_model()
    run_bot()