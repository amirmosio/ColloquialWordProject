import json
import re
import string
from hazm import word_tokenize, Lemmatizer
######################
### configuration ####
######################
from constants import Configs
from tqdm import tqdm


############################
##### random initializer ###
############################


class PreprocessUtilities:
    lemmatizer = Lemmatizer()
    punctuation = string.punctuation + '،؟'

    def __init__(self, stop_words):
        self.stop_words = stop_words if stop_words else []
        self.end_of_sentence_sings = [".", "?", "؟", "!", ";", "؛", ":", "\n"]

        self.pre_processing_functions = [self.remove_emoji_from_text,
                                         self.remove_english_char_from_text,
                                         self.remove_signs,
                                         self.remove_digits_and_replace_digits_sign,
                                         self.remove_url_from_text,
                                         self.remove_extra_spaces,
                                         self.remove_half_space,
                                         self.remove_inflections]

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
    def remove_digits_and_replace_digits_sign(text):
        return re.sub(r'[0-9|۰-۹]+', '#Digits#', text, flags=re.MULTILINE)

    @staticmethod
    def remove_english_char_from_text(text):
        return re.sub(r'[a-zA-Z]', ' ', text, flags=re.MULTILINE)

    @staticmethod
    def remove_signs(text):
        for char in PreprocessUtilities.punctuation:
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

    @staticmethod
    def tokenize_text(text):
        return text.split()

    def process_context(self, context, remove_stop_words=True):
        for proc in self.pre_processing_functions:
            context = proc(context)
        if remove_stop_words:
            return self.remove_stop_words(self.tokenize_text(context))
        return self.tokenize_text(context)


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

    def bring_processed_formal_tokens(self, file_index: int):
        for context in self._load_raw_formal_data(file_index):
            yield self.preprocess_utils.process_context(context)

    def bring_processed_colloquial_tokens(self):
        for context in self._load_raw_colloquial_data():
            yield self.preprocess_utils.process_context(context)

    def _load_raw_formal_data(self, file_index):
        with open(self.formal_directory_path + self.formal_file_paths[file_index], 'rb') as file:
            context_count = 0
            for article in file:
                article = article.decode('utf-8')
                if article != "":
                    for context in json.loads(article)['Text'].split("\n"):
                        context_count += 1
                        yield context
                    if Configs.DEBUG and context_count >= Configs.test_context_number:
                        break

    def _load_raw_colloquial_data(self):
        with open(self.colloquial_file_path, 'rb') as file:
            context_count = 0
            for context in file:
                context = context.decode('utf-8').strip()
                if context.startswith("RT : "):
                    context = context[5:]
                context_count += 1
                yield context
                if Configs.DEBUG and context_count >= Configs.test_context_number:
                    break


if __name__ == '__main__':
    # FormalAndColloquialDataPreProcessing.formal_directory_path = "data/formal_dataset/"
    # FormalAndColloquialDataPreProcessing.stop_words_file_path = "data/stop_words.json"
    # for i in FormalAndColloquialDataPreProcessing()._load_raw_formal_data(1):
    #     print(i)

    FormalAndColloquialDataPreProcessing.colloquial_file_path = "data/colloquial_dataset/lscp-0.5-fa.txt"
    FormalAndColloquialDataPreProcessing.stop_words_file_path = "data/stop_words.json"
    for i in FormalAndColloquialDataPreProcessing()._load_raw_colloquial_data():
        print(i)
