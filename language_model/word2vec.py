import json
import random
import re
import string

import numpy as np
import torch
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

############################
##### random initializer ###
############################


torch.manual_seed(11747)
random.seed(17757)
np.random.seed(7171757)
######################
### configuration ####
######################
debug_mode = False
test_context_number = 10000
device = torch.device("cuda" if torch.cuda.is_available() and not debug_mode else "cpu")
print(f"device: {device}")


############################
## load and tokenize data utils ##
############################
class FormalAndColloquialDataPreProcessing:
    formal_directory_path = "data/formal_dataset/"
    formal_file_paths = ['fawiki-20181001-pages-articles-multistream 1 - 100000.json',
                         'fawiki-20181001-pages-articles-multistream 100001 - 290169.json',
                         'fawiki-20181001-pages-articles-multistream 290170 - 580338.json',
                         'fawiki-20181001-pages-articles-multistream 580339 - 870507.json',
                         'fawiki-20181001-pages-articles-multistream 870508 - 1160676.json']
    colloquial_file_path = 'data/colloquial_dataset/lscp-0.5-fa.txt'
    stop_words_file_path = 'data/stop_words.json'

    def __init__(self):
        self.pre_processing_functions = [self.remove_emoji_from_text,
                                         self.remove_english_char_from_text,
                                         self.remove_signs,
                                         self.remove_url_from_text, self.remove_extra_spaces]
        with open(self.stop_words_file_path, 'rb') as file:
            self.stop_words = json.loads(file.read())['stopWords']

    def bring_processed_formal_tokens(self, file_index: int):
        # tokenize
        data = self._load_raw_formal_data(file_index)
        for context_id in range(len(data)):
            for proc in self.pre_processing_functions:
                data[context_id] = proc(data[context_id])
        return [self.remove_stop_words(self.tokenize_text(context)) for context in data]

    def bring_processed_colloquial_tokens(self):
        # tokenize
        data = self._load_raw_colloquial_data()
        for context_id in range(len(data)):
            for proc in self.pre_processing_functions:
                data[context_id] = proc(data[context_id])
        return [self.remove_stop_words(self.tokenize_text(context)) for context in data]

    def _load_raw_formal_data(self, file_index):
        with open(self.formal_directory_path + self.formal_file_paths[file_index], 'rb') as file:
            data_texts = []
            for article in file:
                article = article.decode('utf-8')
                if article != "":
                    for context in json.loads(article)['Text'].split("\n"):
                        data_texts.append(context)
                if debug_mode and len(data_texts) >= test_context_number:
                    break
        return data_texts

    def _load_raw_colloquial_data(self):
        with open(self.colloquial_file_path, 'rb') as file:
            data_texts = []
            for context in file:
                context = context.decode('utf-8').strip()
                if context.startswith("RT : "):
                    context = context[5:]
                data_texts.append(context)
                if debug_mode and len(data_texts) >= test_context_number:
                    break
        return data_texts

    @staticmethod
    def tokenize_text(text):
        return text.split()

    @staticmethod
    def remove_emoji_from_text(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' ', text)

    @staticmethod
    def remove_url_from_text(text):
        return re.sub(r'^https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)

    @staticmethod
    def remove_english_char_from_text(text):
        return re.sub(r'[a-zA-Z]', ' ', text, flags=re.MULTILINE)

    @staticmethod
    def remove_signs(text):
        for char in string.punctuation:
            text = text.replace(char, ' ')
        return text

    @staticmethod
    def remove_extra_spaces(text):
        return re.sub(r'\s+', ' ', text, flags=re.MULTILINE)

    def remove_stop_words(self, tokens):
        res = []
        for token in tokens:
            if token not in self.stop_words:
                res.append(token)
        return res


##########################
### training word2vec ####
##########################
class CallBack(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

    def on_train_begin(self, model):
        print('Training began ...')
        pass

    def on_epoch_end(self, model):
        self.epoch += 1
        print(self.epoch, " form ", model.epochs)


def initial_train_word2vec():
    formal_tokens = provider.bring_processed_formal_tokens(0)
    colloquial_tokens = provider.bring_processed_colloquial_tokens()
    model = Word2Vec(sentences=formal_tokens + colloquial_tokens, vector_size=200, window=5, workers=4, epochs=10,
                     callbacks=(CallBack(),))
    model.save("word2vec.model")


def train_extra_files(file_index, model=None):
    if model is None:
        model = Word2Vec.load("word2vec.model")
    formal_tokens = provider.bring_processed_formal_tokens(file_index)
    model.train(formal_tokens, total_examples=1, epochs=1)
    model.save("word2vec.model")
    return model


def manual_tests(model=None):
    if model is None:
        model = Word2Vec.load("word2vec.model")
    res = ["احمق", "افسرده", "بیهوش", "باهوش", "تاریک", "طولانی", "پیراهن", "تشک", "قشنگ"]
    res += ["دیوونه", "موندن", "کرمون", "برین", "بزنگ", "تاحالا", "یه", "داش", "تو", "توی", "یکم", "معتاد"]
    for word in res:
        print("############")
        try:
            vector = model.wv[word]  # get numpy vector of a word
            print(word)
            print([i[0] for i in model.wv.most_similar(word, topn=8)])
        except:
            pass


if __name__ == '__main__':
    provider = FormalAndColloquialDataPreProcessing()
    # initial_train_word2vec()
    model = train_extra_files(1)
    model = train_extra_files(2, model=model)
    model = train_extra_files(3, model=model)
    model = train_extra_files(4, model=model)

    manual_tests(model=model)
