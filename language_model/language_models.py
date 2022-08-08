from hazm import Lemmatizer

from global_string_alignmenet import get_normalized_score
from hooshvare_bert import BertLanguageModelService
from word2vec import Word2VecLanguageModelService


class LanguageModelService:
    def __init__(self):
        self.word2vec_service = Word2VecLanguageModelService()
        self.bert_service = BertLanguageModelService()
        self.lemmer = Lemmatizer()
        self.new_text_learned = 0

    def get_colloq_question_if_exists(self, sentence):
        e = 0.000001

        tokens = [self.lemmer.lemmatize(w, pos="PRO") for w in sentence.split()]
        for index, token in enumerate(tokens):
            if token not in self.word2vec_service.formal_tokens:
                scores = {}
                similar_words = self.word2vec_service.get_similar_words_from_formal_or_both(token,
                                                                                            just_return_formals=True)
                if similar_words:
                    masked_sentence = " ".join(
                        [("[MASK]" if i == index else w) for i, w in enumerate(sentence.split())])
                    for word, word2vec_score in similar_words.items():
                        align_score = get_normalized_score(token, word) + e
                        bert_score = self.bert_service.get_prediction_score_with_fill_mask(masked_sentence, word) + e
                        scores[word] = align_score * bert_score * (word2vec_score + e)
                    return token, scores

    def train_model_with_new_sentence_and_save_eventually(self, sentence):
        tokens = [self.lemmer.lemmatize(w, pos="PRO") for w in sentence.split()]
        self.word2vec_service.train_new_text(tokens, epoch=1)
        self.bert_service.train_new_text(tokens)

        self.new_text_learned += 1
        if self.new_text_learned >= 100:
            self.word2vec_service.save_model()
            self.bert_service.save_model()
            self.new_text_learned = 0
