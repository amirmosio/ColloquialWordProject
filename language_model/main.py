import json

import numpy as np
from hazm import Lemmatizer

from data_load_and_processing import FormalAndColloquialDataPreProcessing
from hooshvare_bert import fill_mask, word_vector_in_context
from word2vec import LanguageModelService

if __name__ == '__main__':

    """
    test combine model
    """
    """
    initial address config
    """
    LanguageModelService.model_path = "word2vec.model"
    LanguageModelService.formal_tokens_path = "formal_tokens.json"
    FormalAndColloquialDataPreProcessing.formal_directory_path = "data/formal_dataset/"
    FormalAndColloquialDataPreProcessing.colloquial_file_path = 'data/colloquial_dataset/lscp-0.5-fa.txt'
    FormalAndColloquialDataPreProcessing.stop_words_file_path = 'data/stop_words.json'
    language_model_service = LanguageModelService()
    LanguageModelService.model_path = "word2vec_test.model"
    with open("dev_test.json", 'rb') as dev_data:
        sample_sentences = json.loads(dev_data.read())
    lemer = Lemmatizer()

    for word in ["کرمون"]:
        print("\nNew Word")
        print(word, end="==> ")
        similar_words = language_model_service.get_similar_words_from_formal_or_both(word,
                                                                                     just_return_formals=True)
        similar_words = list(similar_words.keys())
        for suggested_word in similar_words:
            print(suggested_word, end=":")
            scores = []
            for sentence in sample_sentences[word]:
                tokens = [lemer.lemmatize(w) for w in sentence.split()]
                prediction = fill_mask(sentence, targets=[suggested_word])[0]
                scores.append(float("%.7f" % prediction['score']))
            print(np.array(scores).prod(), np.array(scores).sum())
        print()
    print("." * 50)
    res = ["احمق", "افسرده", "بیهوش", "باهوش", "تاریک", "طولانی", "پیرهن", "تشک", "قشنگ"]
    res += ["دیوونه", "موندن", "کرمون", "برین", "بزنگ", "تاحالا", "یه", "داش", "تو", "توی", "یکم", "معتاد"]
    for word in res:
        print("w" * 10)
        print(word)
        similar_words = language_model_service.get_similar_words_from_formal_or_both(word,
                                                                                     just_return_formals=True)
        print(similar_words, end=": ")
        word_vector = word_vector_in_context(word, 0)
        for sim_word in list(similar_words.keys()):
            sim_word_vector = word_vector_in_context(sim_word, 0)
            dist = sum(((word_vector - sim_word_vector) ** 2).squeeze())
            print(f"w{sim_word}w: {similar_words[sim_word]} - {dist}", end="|")
        print()
