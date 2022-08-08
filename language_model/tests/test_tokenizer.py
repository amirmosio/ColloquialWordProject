from hazm import Lemmatizer

sentence = "کرمون مکان های دیدنی بسیاری دارد."
lemer = Lemmatizer()
tokens = [lemer.lemmatize(w) for w in sentence.split()]
print(tokens)
