class OutPutMessages:
    @staticmethod
    def start_message_with_channel(channels):
        res = (
                "سلام" + "\n" +
                "با این بات می تونی یکی از کانال های پیشنهادیمون رو انتخاب کنی و ما برات آهنگ های خوبش رو می فرستیم." +
                "\n" + "مطابق با ژانر مورد علاقت یکی رو انتخاب کن:" +
                "\n")
        res += " - ".join([f"@{ch}" for ch in channels])
        return res

    @staticmethod
    def good_choice_music_condition(selected_channel, channel_music_count):
        res = (
                f"@{selected_channel}" + "\n" + "به به" + "! " +
                "آهنگ های مورد انتخابی به صورت اتوماتیک و با الگوریتم ساده ای انتخاب می شن." +
                "\n"
                f"تعداد کا آهنگ های این کانال در حال حاضر {channel_music_count} تاست."
                + "\n"
                + f"از این به بعد هر بار که /gimme رو بفرستی برات یکی از آهنگ های خوب {selected_channel} رو می فرستم." +
                "\n")
        return res

    about_us = "ما قصدمون از ایجاد این بات این بوده که بتونیم یک مدل زبانی و دیتاستی از کلمات محاوره ای زبان فارسی " \
               "ایجاد کنیم. "
    select_one_of_channels = "اول /start رو بزن و یکی از کانال ها رو انتخاب کن."

    @staticmethod
    def which_one_has_the_closest_meaning(word):
        return "کدومشون نزدیک ترین معنی رسمی رو به" + f"\"{word}\"" + "داره؟" + "\n" + "تاحالا ندیده بودمش!"

    none_of_the_above_options = "هیچکدومشون"


if __name__ == '__main__':
    print(OutPutMessages.start_message_with_channel(["sss", "sdfsg"]))
