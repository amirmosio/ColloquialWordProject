from data_load_and_processing import FormalAndColloquialDataPreProcessing
from word2vec import Word2VecLanguageModelService

if __name__ == '__main__':
    """
    load formal tokens and save them
    """
    # language_model_service = LanguageModelService(load_model=False)
    # LanguageModelService.formal_tokens_path_load = "formal_tokens_test.json"
    # language_model_service.process_all_formal_tokens_and_save()
    # language_model_service.load_formal_tokens_json()
    # print(language_model_service.formal_tokens)
    """
    test w2v model
    """

    language_model_service = Word2VecLanguageModelService()

    res = ["احمق", "افسرده", "بیهوش", "باهوش", "تاریک", "طولانی", "پیرهن", "تشک", "قشنگ"]
    res += ["دیوونه", "موندن", "کرمون", "برین", "بزنگ", "تاحالا", "یه", "داش", "تو", "توی", "یکم", "معتاد"]
    for w in res:
        print(w)
        print(language_model_service.get_similar_words_from_formal_or_both(w, just_return_formals=True))
    test_text = "یجوری حرف بزن بفهمیم."
    test_tokens = language_model_service.provider.preprocess_utils.process_context(test_text)
    # cosmul does not seem to be a good function for similar vectors
    print(language_model_service.model.wv.most_similar_cosmul(positive=["یجوری", "یجوری", "یجوری"],
                                                              negative=["یهو", "مث"], topn=20))
    print(language_model_service.model.wv.most_similar(positive=["یجوری", "یجوری", "یجوری"],
                                                       negative=["یهو", "مث"], topn=20))

    sims = language_model_service.get_similar_words_from_formal_or_both("سسبلیبایال")
    print(sims)

    new_text = "سلام بر سسبلیبایال زیبا"
    tokens = language_model_service.provider.preprocess_utils.process_context(new_text)
    print(len(language_model_service.model.wv))

    language_model_service.train_new_text([tokens], epoch=100)

    sims = language_model_service.get_similar_words_from_formal_or_both("سسبلیبایال")
    print(sims)
    print(len(language_model_service.model.wv))
