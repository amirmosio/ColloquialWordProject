import json
import re
import string
from hazm import word_tokenize, Lemmatizer
######################
### configuration ####
######################
from constants import Constants

############################
##### random initializer ###
############################

test_context_number = 10000


class PreprocessUtilities:
    lemmatizer = Lemmatizer()

    def __init__(self, stop_words=None):
        self.stop_words = stop_words if stop_words else []
        self.end_of_sentence_sings = [".", "?", "؟", "!", ";", "؛", ":"]

    def split_sentences(self, text):
        return re.split(f"|".join(["\\" + i for i in self.end_of_sentence_sings]), text)

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

    @staticmethod
    def remove_half_space(text):
        return re.sub(r'\u200c', ' ', text, flags=re.MULTILINE)

    @staticmethod
    def remove_inflections(text):
        tokens = word_tokenize(text)
        lemma_tokens = [PreprocessUtilities.lemmatizer.lemmatize(w) for w in tokens]
        return " ".join(lemma_tokens)


class FormalAndColloquialDataPreProcessing:
    formal_directory_path = "language_model/data/formal_dataset/"
    formal_file_paths = ['fawiki-20181001-pages-articles-multistream 1 - 100000.json',
                         'fawiki-20181001-pages-articles-multistream 100001 - 290169.json',
                         'fawiki-20181001-pages-articles-multistream 290170 - 580338.json',
                         'fawiki-20181001-pages-articles-multistream 580339 - 870507.json',
                         'fawiki-20181001-pages-articles-multistream 870508 - 1160676.json']
    colloquial_file_path = 'language_model/data/colloquial_dataset/lscp-0.5-fa.txt'
    stop_words_file_path = 'language_model/data/stop_words.json'

    def __init__(self):
        with open(self.stop_words_file_path, 'rb') as file:
            stop_words = json.loads(file.read())['stopWords']
        self.preprocess_utils = PreprocessUtilities(stop_words)
        self.pre_processing_functions = [self.preprocess_utils.remove_emoji_from_text,
                                         self.preprocess_utils.remove_english_char_from_text,
                                         self.preprocess_utils.remove_signs,
                                         self.preprocess_utils.remove_url_from_text,
                                         self.preprocess_utils.remove_extra_spaces,
                                         self.preprocess_utils.remove_half_space]

    def bring_custom_text_tokens(self, custom_text):
        for proc in self.pre_processing_functions:
            custom_text = proc(custom_text)
        return [self.tokenize_text(custom_text)]

    def bring_processed_formal_tokens(self, file_index: int):
        # tokenize
        data = self._load_raw_formal_data(file_index)
        for context_id in range(len(data)):
            for proc in self.pre_processing_functions:
                data[context_id] = proc(data[context_id])
            yield self.preprocess_utils.remove_stop_words(self.tokenize_text(data[context_id]))

    def bring_processed_colloquial_tokens(self):
        # tokenize
        data = self._load_raw_colloquial_data()
        for context_id in range(len(data)):
            for proc in self.pre_processing_functions:
                data[context_id] = proc(data[context_id])
        return [self.preprocess_utils.remove_stop_words(self.tokenize_text(context)) for context in data]

    def _load_raw_formal_data(self, file_index):
        with open(self.formal_directory_path + self.formal_file_paths[file_index], 'rb') as file:
            data_texts = []
            for article in file:
                article = article.decode('utf-8')
                if article != "":
                    for context in json.loads(article)['Text'].split("\n"):
                        data_texts.append(context)
                    if Constants.DEBUG and len(data_texts) >= test_context_number:
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
                if Constants.DEBUG and len(data_texts) >= test_context_number:
                    break
        return data_texts

    @staticmethod
    def tokenize_text(text):
        return text.split()


if __name__ == '__main__':
    # FormalAndColloquialDataPreProcessing.formal_directory_path = "data/formal_dataset/"
    # FormalAndColloquialDataPreProcessing.stop_words_file_path = "data/stop_words.json"
    # for i in FormalAndColloquialDataPreProcessing()._load_raw_formal_data(1):
    #     print(i)

    FormalAndColloquialDataPreProcessing.colloquial_file_path = "data/colloquial_dataset/lscp-0.5-fa.txt"
    FormalAndColloquialDataPreProcessing.stop_words_file_path = "data/stop_words.json"
    for i in FormalAndColloquialDataPreProcessing()._load_raw_colloquial_data():
        print(i)
