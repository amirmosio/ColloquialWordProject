import json
import random

import numpy as np
import torch
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

from config import DEBUG_MODE
############################
##### random initializer ###
############################
from data_load_and_processing import FormalAndColloquialDataPreProcessing

torch.manual_seed(11747)
random.seed(17757)
np.random.seed(7171757)

######################
### configuration ####
######################
test_context_number = 10000
device = torch.device("cuda" if torch.cuda.is_available() and not DEBUG_MODE else "cpu")
print(f"device: {device}")


##########################
### training word2vec ####
##########################
class LanguageModelService:
    model_path = "language_model/word2vec.model"
    formal_tokens_path = "language_model/formal_tokens.json"
    epochs = 10

    class CallBack(CallbackAny2Vec):
        def __init__(self):
            self.epoch = 0

        def on_train_begin(self, model):
            print('Training began ..., it may take a while!')
            pass

        def on_epoch_end(self, model):
            self.epoch += 1
            print(str(self.epoch) + "\\" + str(model.epochs), end=" - " if self.epoch != model.epochs else "\n")

    def __init__(self, load_model=True):
        self.provider = FormalAndColloquialDataPreProcessing()
        self.model = self.load_model() if load_model else None
        self.formal_tokens = self.load_formal_tokens_json() if load_model else set()

    def load_model(self):
        return Word2Vec.load(self.model_path)

    def save_model(self):
        if not DEBUG_MODE:
            self.model.save(self.model_path)

    def train_new_text(self, tokens, epoch=None):
        self.model.min_count = 1
        self.model.train(tokens, total_examples=len(tokens), epochs=epoch if epoch else self.epochs,
                         callbacks=(self.CallBack(),))
        self.save_model()

    def train_model(self):

        all_tokens = self.provider.bring_processed_colloquial_tokens()
        for i in range(5):
            all_tokens += self.provider.bring_processed_formal_tokens(i)
        self.model = Word2Vec(sentences=all_tokens, vector_size=200, window=5, workers=4, epochs=self.epochs,
                              callbacks=(self.CallBack(),), min_count=1)
        self.save_model()

    """
    Formal Tokens List
    """

    def process_all_formal_tokens_and_save(self):
        for i in range(5):
            tokens = self.provider.bring_processed_formal_tokens(i)
            for context in tokens:
                self.formal_tokens.update(context)

        with open(LanguageModelService.formal_tokens_path, 'w') as file:
            file.write(json.dumps(list(self.formal_tokens)))

    @classmethod
    def load_formal_tokens_json(cls):
        with open(cls.formal_tokens_path, 'rb') as file:
            formal_tokens = json.loads(file.read())
        return formal_tokens

    def get_similar_words_from_formal_or_both(self, positive=None, negative=None, topn=8, just_return_formals=True):
        try:
            res = {}
            coeff_constant = 4  # maybe a good estimates for colloquial_tokens/formal_tokens
            while len(res) != topn:
                for token, distance in self.model.wv.most_similar(positive=positive, negative=negative,
                                                                  topn=topn * coeff_constant):
                    if token not in res and (not just_return_formals or token in self.formal_tokens):
                        res[token] = round(distance, 3)
                        if len(res) == topn:
                            break
                coeff_constant *= 2
            return res
        except:
            return None

    """
    Unknown Colloquial Tokens
    """

    def get_back_interesting_token_and_similar_words(self, text):
        text_tokens = self.provider.bring_custom_text_tokens(text)[0]
        for token in text_tokens:
            if token not in self.formal_tokens:
                sim_words = self.get_similar_words_from_formal_or_both(token, topn=9)
                if sim_words:
                    return token, sim_words
        return None, None
