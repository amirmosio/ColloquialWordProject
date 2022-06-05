import json
import re
import string

from config import DEBUG_MODE

############################
##### random initializer ###
############################

######################
### configuration ####
######################
test_context_number = 10000


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
        self.pre_processing_functions = [self.remove_emoji_from_text,
                                         self.remove_english_char_from_text,
                                         self.remove_signs,
                                         self.remove_url_from_text, self.remove_extra_spaces, self.remove_half_space]
        with open(self.stop_words_file_path, 'rb') as file:
            self.stop_words = json.loads(file.read())['stopWords']

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
            yield self.remove_stop_words(self.tokenize_text(data[context_id]))

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
                    if DEBUG_MODE and len(data_texts) >= test_context_number:
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
                if DEBUG_MODE and len(data_texts) >= test_context_number:
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

    @staticmethod
    def remove_half_space(text):
        # TODO
        return text
        # return re.sub(r'\u200c', ' ', text, flags=re.MULTILINE)
