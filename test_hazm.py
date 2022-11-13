from hazm import Stemmer, word_tokenize, sent_tokenize, Lemmatizer

if __name__ == '__main__':
    test_words = ["کتاب‌ها", "می روم", "بزنگها", "ناها", "شاها", "یجوری", "تنها", "بچه‌ها", "عوضی", "بدبخت", "حالش",
                  "بداخلاق", "کلافه", "افسردگی", "بی\u200cحسی", "باهوش،", "سرگیجه", "باهوشتر", "باهوشی", "تیرگی",
                  "ستاره\u200cها", "تاریک\u200cترین", "روشنایی", "می\u200cتابد", "طولانی\u200cمدت", "زیادی",
                  "مسافت\u200cهای", "کوتاهی", "پیراهنش", "کالسکه", "عاشقم", "مونه", "کرمون", "برین", "بکشید", "میدما",
                  "نکردم", "عجیبه", "نگفته", "هنو", "داشی", "توی", "یکمی", "اعتیادش"]
    stemmer = Stemmer()
    for w in test_words:
        print(f"{w}:{stemmer.stem(w)}")

    print(word_tokenize('منتها برای پردازش، جدا بهتر نیست؟'))
    print(sent_tokenize('منتها برای پردازش، جدا بهتر نیست؟'))

    lemer = Lemmatizer()
    for w in test_words:
        print(f"{w}:{lemer.lemmatize(w)}")
    # https: // www.thepythoncode.com / article / pretraining - bert - huggingface - transformers - in -python
