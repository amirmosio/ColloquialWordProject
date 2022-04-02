from data_load_and_processing import FormalAndColloquialDataPreProcessing
from word2vec import LanguageModelService

if __name__ == '__main__':
    # initial address config
    LanguageModelService.model_path = "word2vec.model"
    LanguageModelService.formal_tokens_path = "formal_tokens.json"
    FormalAndColloquialDataPreProcessing.formal_directory_path = "data/formal_dataset/"
    FormalAndColloquialDataPreProcessing.colloquial_file_path = 'data/colloquial_dataset/lscp-0.5-fa.txt'
    FormalAndColloquialDataPreProcessing.stop_words_file_path = 'data/stop_words.json'

    # load formal tokens and save them
    # language_model_service = LanguageModelService()
    # language_model_service.process_all_formal_tokens_and_save()
    # language_model_service.load_formal_tokens_json()
    # print(language_model_service.formal_tokens)

    # train model

    # test model

    language_model_service = LanguageModelService()
    LanguageModelService.model_path = "word2vec_test.model"

    res = ["احمق", "افسرده", "بیهوش", "باهوش", "تاریک", "طولانی", "پیرهن", "تشک", "قشنگ"]
    res += ["دیوونه", "موندن", "کرمون", "برین", "بزنگ", "تاحالا", "یه", "داش", "تو", "توی", "یکم", "معتاد"]
    for w in res:
        print(w)
        print(language_model_service.get_similar_words_from_formal_or_both(w, just_return_formals=False))
    test_text = "یجوری حرف بزن بفهمیم."
    test_tokens = language_model_service.provider.bring_custom_text_tokens(test_text)
    # cosmul does not seem to be a good function for similar vectors
    print(language_model_service.model.wv.most_similar_cosmul(positive=["یجوری", "یجوری", "یجوری"],
                                                              negative=["یهو", "مث"], topn=20))
    print(language_model_service.model.wv.most_similar(positive=["یجوری", "یجوری", "یجوری"],
                                                       negative=["یهو", "مث"], topn=20))

    sims = language_model_service.get_similar_words_from_formal_or_both("سسبلیبایال")
    print(sims)

    new_text = "سلام بر سسبلیبایال زیبا"
    tokens = language_model_service.provider.bring_custom_text_tokens(new_text)
    print(len(language_model_service.model.wv))

    language_model_service.model.build_vocab(tokens, update=True)
    language_model_service.train_new_text(tokens, epoch=100)

    sims = language_model_service.get_similar_words_from_formal_or_both("سسبلیبایال")
    print(sims)
    print(len(language_model_service.model.wv))
