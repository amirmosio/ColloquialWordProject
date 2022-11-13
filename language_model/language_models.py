from config import Configs
from utils.global_string_alignmenet import get_normalized_score
from hooshvare_bert import BertLanguageModelService
from word2vec import Word2VecLanguageModelService
import threading


#
# class DelayedThread(threading.Thread):
#     def __init__(self, word2vec_service, corpus_iterable, thread_lock):
#         threading.Thread.__init__(self)
#         self._stop = threading.Event()
#         self.word2vec_service = word2vec_service
#         self.corpus_iterable = corpus_iterable
#         self.thread_lock = thread_lock
#
#     def run(self):
#         self.thread_lock.acquire()
#
#         self.word2vec_service.train_new_text(self.corpus_iterable, epoch=1)
#         self.word2vec_service.save_model()
#
#         self.thread_lock.release()


class LanguageModelService:
    def __init__(self):
        self.word2vec_service = Word2VecLanguageModelService()
        self.bert_service = BertLanguageModelService()

        self.new_text_to_train_queue = []
        self.threadLock = threading.Lock()

    def _get_token_and_scores_for_colloq_in_context(self, token, index, tokens):
        e = 0.000001
        scores = {}
        similar_words = self.word2vec_service.get_similar_words_from_formal_or_both(token, just_return_formals=True)
        if similar_words:
            masked_sentence = " ".join([("[MASK]" if i == index else w) for i, w in enumerate(tokens)])
            for word, word2vec_score in similar_words.items():
                align_score = get_normalized_score(token, word)
                bert_score = self.bert_service.get_prediction_score_with_fill_mask(masked_sentence, word)
                scores[word] = align_score + bert_score + e
            return token, scores

    def get_colloq_question_if_exists(self, tokens_list):
        for index, token in enumerate(tokens_list):
            if token not in self.word2vec_service.formal_tokens:
                res = self._get_token_and_scores_for_colloq_in_context(token, index, tokens_list)
                if res: return res

    def train_model_with_new_sentence_and_save_eventually(self, tokens_list):
        self.new_text_to_train_queue.append(tokens_list)
        if len(self.new_text_to_train_queue) >= Configs.train_max_queue_length:
            corpus_iterable_copy = [item for item in self.new_text_to_train_queue]
            # self.bert_service.train_new_text(tokens)
            # self.bert_service.save_model()
            # train_thread = DelayedThread(self.word2vec_service, corpus_iterable_copy, self.threadLock)
            # train_thread.start()
            self.word2vec_service.train_new_text(corpus_iterable_copy, epoch=1)
            self.word2vec_service.save_model()
            self.new_text_to_train_queue = []
