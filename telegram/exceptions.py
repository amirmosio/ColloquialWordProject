from constants import OutPutMessages


class _MyExceptions(Exception):
    def __init__(self, message):
        self.message = message


class IntroducerNotFound(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.introducer_not_found)


class YouIntroducedThisUserCanNotBeenIntroducer(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.you_introduced_this_user_select_other_user)


class AlreadyHasIntroducer(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.already_has_introducer)


class UserNotFound(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.user_not_found_start_first)


class AnsweredBeforeByTheUser(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.you_have_answered_this_before)


class DoneBefore(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.done_before)


class NoQuestionReadyToAnswerWait(_MyExceptions):
    def __init__(self):
        super().__init__(OutPutMessages.no_question_ready_for_you_wait)


def handle_my_exceptions_for_telegram_bot(bot):
    def func_creator(func):
        async def func_wrapper(message):
            chat_id = message.chat.id
            try:
                return await func(message)
            except Exception as e:
                if isinstance(e, _MyExceptions):
                    await bot.send_message(chat_id=chat_id, text=e.message)
                else:
                    print("handle_my_exceptions_for_telegram_bot")
                    print(e)
                    await bot.send_message(chat_id=chat_id, text=OutPutMessages.internal_error_call_support)

        return func_wrapper

    return func_creator


def handle_my_exceptions_print():
    def func_creator(func):
        async def func_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print("handle_my_exceptions_print")
                print(e)

        return func_wrapper

    return func_creator
