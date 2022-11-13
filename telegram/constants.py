from config import Configs


def _lined(list_string):
    return "\n".join(list_string)


class Commands:
    start = "start"
    about_us = "about_us"
    # music = "music"
    question = "question"
    show_channels = "show_channels"


class OutPutMessages:

    @staticmethod
    def start_message():
        res = _lined(["با این بات می تونی امتیاز کسب کنی، کد تخفیف های مختلف و آهنگ های باحال بگیری.",
                      f"برای پاسخ به سوال هامون با هر دفعه فرستادن /{Commands.question} ما برات یک سوال ارسال می کنیم.",
                      # f"برای دریافت موسیقی های پیشنهادیمون هم در صورتی که امتیاز کافی داشته باشی می تونی /{Commands.music} رو ارسال کنی."
                      ])
        return res

    set_introducer_button = "معرف"

    @staticmethod
    def introducer_has_been_set(introducer_username):
        return f" معرف شما {Configs.introduce_score} امتیاز گرفت. "

    send_introducer_user_name = _lined(["حالا نام کاربری معرفت رو بفرست که امتیاز بگیره.به این شکل:", "@username"])
    wrong_format_for_username = "فرمت نام کاربری اشتباه است"
    you_have_introduced_a_user = _lined(["تبریک", f"معرف یک نفر شدید و {Configs.introduce_score} امتیاز گرفتید."])
    #
    # @staticmethod
    # def use_score_to_get_music(channels):
    #     res = ("""حالا می تونی یکی از کانال های پیشنهادیمون رو انتخاب کنی
    #             و با امتیاز هایی که داری، ما برات آهنگ های خوبش رو می فرستیم.
    #            مطابق با ژانر مورد علاقت یکی رو انتخاب کن:
    #            \n""")
    #     res += " - ".join([f"@{ch}" for ch in channels])
    #     return res

    # @staticmethod
    # def good_choice_music_condition(selected_channel, channel_music_count):
    #     res = (
    #             f"@{selected_channel}" + "\n" + "به به" + "! " +
    #             "آهنگ های مورد انتخابی به صورت اتوماتیک و با الگوریتم ساده ای انتخاب می شن." +
    #             "\n"
    #             f"تعداد آهنگ های این کانال در حال حاضر {channel_music_count} تاست."
    #             + "\n"
    #             + f"از این به بعد هر بار که /{Commands.music} رو بفرستی برات یکی از آهنگ های خوب {selected_channel} رو می فرستم." +
    #             "\n")
    #     return res

    about_us = _lined([
        "ما قصدمون از ایجاد این بات این بوده که بتونیم یک مدل زبانی و دیتاستی از کلمات محاوره ای زبان فارسی ایجاد کنیم.",
        "با این بات شما می تونید به سوال هامون جواب بدید و به کامل شدن داده هامون کمک کنید،",
        " امتیاز کسب کنید و ما برای تشویق در پایان دوره ها به صورت تصادفی کد های تخفیف و جوایزی رو در نظر می گیریم."
        f"مطمین شو در پایان دوره حداقل امتیاز {Configs.min_score_for_lottery} رو داری تا بتونی در قرعه کشی شرکت کنی."])
    select_one_of_channels = f"اول /{Commands.show_channels} رو بزن و یکی از کانال ها رو انتخاب کن."

    @staticmethod
    def which_one_has_the_closest_meaning(word):
        return _lined(["کدومشون نزدیک ترین معنی رسمی رو به" + f"\"{word}\"" + "داره؟"])

    @staticmethod
    def question_options(options):
        return _lined([f"/{i} {options[i]}" for i in range(10)])

    none_of_the_above_options = "هیچکدام"

    introducer_not_found = "معرف رو پیدا نمی کنم!"
    already_has_introducer = "معرف قبلا ذخیره شده!"
    you_introduced_this_user_select_other_user = _lined(
        ["شما این کاربر رو معرفی کردید.", "کاربر دیگری رو به عنوان معرف انتخاب کنید!"])

    not_enough_credit_answer_question_to_get = _lined(
        ["امتیاز کافی برای دریافت موزیک نداری. برای بدست آوردن امتیاز دو راه وجود داره:",
         "- نام کاربری تلگرامت رو به دوستات بدی که به عنوان معرف وارد کنن." + f" {Configs.introduce_score}$ ",
         "🤝",
         "- به سوالات هم معنی خیلی سادمون جواب بدی." + f" {Configs.question_answer_score}$ ",
         f"🤗 /{Commands.question}"
         ])
    user_not_found_start_first = _lined(["کاربر رو پیدا نمی کنم.", f"از /{Commands.start} شروع کن."])
    you_have_answered_this_before = _lined(["به این سوال قبلا جواب دادید!"])
    done_before = _lined(["به این سوال قبلا جواب دادید!"])

    @staticmethod
    def state_pinned_message(introducer, select_music_channel, score):
        return _lined([
            f"{score}$" + " | " + f"معرف: {('@' + introducer) if introducer else '-'}"
            # f"کانال موسیقی: {('@' + select_music_channel) if select_music_channel else '-'}"

        ])

    no_question_ready_for_you_wait = _lined(["سوال هامون تموم شدن.",
                                             "مدتی صبر کنید تا سوال های جدید ساخته شن!"])

    internal_error_call_support = "خطای داخلی، لطفا با پشتیبانی تماس بگیرید."

    @staticmethod
    def you_gave_a_wrong_answer(question_word):
        return _lined([
            "به نظر به سوال مربوط به کلمه " + f"{question_word} " + "جواب اشتباهی رو ارسال کردی.",
            f"{Configs.question_wrong_answer_score}" + " امتیاز"
        ])
