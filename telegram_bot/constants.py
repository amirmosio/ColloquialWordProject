class OutPutMessages:
    start_message = "سلام"
    about_us = "ما قصدمون از ایجاد این بات این بوده که بتونیم یک مدل زبانی و دیتاستی از کلمات محاوره ای زبان فارسی " \
               "ایجاد کنیم. "

    @staticmethod
    def which_one_has_the_closest_meaning(word):
        return "کدومشون نزدیک ترین معنی رسمی رو به" + f"\"{word}\"" + "داره؟" + "\n" + "تاحالا ندیده بودمش!"

    none_of_the_above_options = "هیچکدومشون"
