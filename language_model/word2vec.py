import json
import random
import time
import numpy as np
import torch
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from itertools import chain, islice
from tqdm import tqdm
############################
##### random initializer ###
############################
from constants import Configs
from data_load_and_processing import FormalAndColloquialDataPreProcessing

torch.manual_seed(11747)
random.seed(17757)
np.random.seed(7171757)


##########################
### training word2vec ####
##########################
class SentencesIterator:
    def __init__(self, generator_function):
        self.generator_function = generator_function
        self.generator = self.generator_function()

    def __iter__(self):
        # reset the generator
        self.generator = self.generator_function()
        return self

    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result


class Word2VecLanguageModelService:
    model_path_save = "language_model/word2vec.model"
    model_path_load = "language_model/word2vec.model19308.model"
    formal_tokens_path_save = "language_model/formal_tokens.json"
    formal_tokens_path_load = "language_model/kaggle_outputs/formal_tokens_merged_with_bert.json"

    class CallBack(CallbackAny2Vec):
        def __init__(self):
            self.epoch = 0

        def on_train_begin(self, model):
            print('Training began ..., it may take a while!')
            pass

        def on_epoch_end(self, model):
            self.epoch += 1
            print(str(self.epoch) + "\\" + str(model.epochs), end=" - " if self.epoch != model.epochs else "\n")
            # model.save(Word2VecLanguageModelService.model_path_save)

    def __init__(self, load_model=True):
        self.provider = FormalAndColloquialDataPreProcessing()
        self.model = self.load_model() if load_model else None
        self.formal_tokens = self.load_formal_tokens_json() if load_model else set()

    def load_model(self):
        return Word2Vec.load(self.model_path_load)

    def save_model(self):
        print(f"Saving model...")
        day = int(time.time() / (24 * 60 * 60))
        self.model.save(self.model_path_save + str(day) + ".model")
        print("Saved.")

    def train_new_text(self, corpus_iterable, epoch=None):
        print(f"Training started on {len(corpus_iterable)} ...")
        self.model.min_count = 1
        self.model.train(corpus_iterable, total_examples=len(corpus_iterable), epochs=epoch)
        self.model.build_vocab(corpus_iterable, update=True)
        print(f"Training finished")

    @staticmethod
    def shuffle(generator, buffer_size=4000):
        count_txt = 0
        while True:
            buffer = list(islice(generator, buffer_size))
            if len(buffer) == 0:
                break
            np.random.shuffle(buffer)
            for item in buffer:
                count_txt += 1
                if count_txt % 10000 == 0:
                    print(10000, end="-")
                yield item

    def train_model(self):
        def get_generator():
            all_tokens_generator = chain(self.provider.bring_processed_colloquial_tokens(),
                                         self.provider.bring_processed_formal_tokens(0),
                                         self.provider.bring_processed_formal_tokens(1),
                                         self.provider.bring_processed_formal_tokens(2),
                                         self.provider.bring_processed_formal_tokens(3),
                                         self.provider.bring_processed_formal_tokens(4))
            return self.shuffle(all_tokens_generator)

        self.model = Word2Vec(sentences=SentencesIterator(get_generator), vector_size=200, window=5, workers=4,
                              epochs=Configs.train_epochs,
                              callbacks=(self.CallBack(),), min_count=1)
        self.save_model()

    """
    Formal Tokens List
    """

    def process_all_formal_tokens_and_save(self):
        for i in tqdm(range(5)):
            for context in tqdm(self.provider.bring_processed_formal_tokens(i)):
                if Configs.DEBUG:
                    for word in ['جوریم', 'دیوونم', 'دیوونس', 'خونس']:
                        if word in context:
                            print("found one!")
                            breakpoint()
                self.formal_tokens.update(context)

        with open(self.formal_tokens_path_save, 'w') as file:
            file.write(json.dumps(list(self.formal_tokens)))

    @classmethod
    def load_formal_tokens_json(cls):
        with open(cls.formal_tokens_path_load, 'rb') as file:
            formal_tokens = json.loads(file.read())
        return set(formal_tokens)

    def get_similar_words_from_formal_or_both(self, positive=None, negative=None, topn=9, just_return_formals=True):
        try:
            res = {}
            coeff_constant = 4  # maybe a good estimates for colloquial_tokens/formal_tokens
            while len(res) != topn and coeff_constant < 2048:
                for token, distance in self.model.wv.most_similar(positive=positive, negative=negative,
                                                                  topn=topn * coeff_constant):
                    if token not in res and (not just_return_formals or token in self.formal_tokens):
                        res[token] = round(1 / distance, 3)
                        if len(res) == topn:
                            break
                coeff_constant *= 2
            return res
        except Exception as e:
            print(f"Error in word2vec get_similar_words {e}")
            return None

    """
    Unknown Colloquial Tokens
    """

    def get_back_interesting_token_and_similar_words(self, text):
        text_tokens = self.provider.preprocess_utils.process_context(text)[0]
        for token in text_tokens:
            if token not in self.formal_tokens:
                sim_words = self.get_similar_words_from_formal_or_both(token, topn=9)
                if sim_words:
                    return token, sim_words
        return None, None
