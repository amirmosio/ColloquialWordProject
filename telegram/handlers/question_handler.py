import telebot

from constants import OutPutMessages, Commands
from exceptions import handle_my_exceptions_for_telegram_bot
from handlers.profile_handler import update_pin_message
from models import ColloquialQuestion


def handler_question(client_bot_handler):
    @client_bot_handler.telebotConf.bot.message_handler(commands=[Commands.question])
    @handle_my_exceptions_for_telegram_bot(client_bot_handler.telebotConf.bot)
    async def give_me_question(message):
        chat_id = message.chat.id
        q: ColloquialQuestion = client_bot_handler.database_utility.select_a_new_question_for_user(message.from_user.id)

        vote_message = OutPutMessages.which_one_has_the_closest_meaning(q.request_word)
        vote_options = [q.get_choice_by_number(i) for i in range(9)]
        vote_options += [OutPutMessages.none_of_the_above_options]

        markup = telebot.types.InlineKeyboardMarkup()
        for i, option in enumerate(vote_options):
            markup.add(telebot.types.InlineKeyboardButton(text=option,
                                                          callback_data=f'selected_option_{i}_{q.id}'))
        await client_bot_handler.telebotConf.bot.send_message(chat_id, vote_message, reply_markup=markup)

    def select_channel_func_condition(call):
        c = call.data.startswith("selected_option_")
        c = c and int(call.data[16:].split("_")[0]) in list(range(10))
        return c

    @client_bot_handler.telebotConf.bot.callback_query_handler(func=select_channel_func_condition)
    async def create_user_answer(call):
        user_id = call.from_user.id

        selected_option = int(call.data[16:].split("_")[0])
        question_id = int(call.data[16:].split("_")[1])
        question = client_bot_handler.database_utility.get_question(question_id)
        client_bot_handler.database_utility.answer_question(question_id, user_id, selected_option)
        # handle wrong answers
        if question.done:
            if question.user_selected_choice != selected_option:
                wrong_user = client_bot_handler.database_utility.get_user(user_id)
                client_bot_handler.database_utility.punish_user_with_wrong_answer(wrong_user)
                await client_bot_handler.telebotConf.bot.send_message(chat_id=wrong_user.chat_id,
                                                                      text=OutPutMessages.you_gave_a_wrong_answer(
                                                                          question.request_word))
                await update_pin_message(client_bot_handler, wrong_user.user_id, wrong_user.chat_id, None)

        else:
            question = client_bot_handler.database_utility.check_question_update_done_with_final_answer_just_get_done(
                question_id)
            if question:
                # question right now, just get done
                wrong_users = client_bot_handler.database_utility.get_question_wrong_answers(question.id)
                for wrong_user in wrong_users:
                    client_bot_handler.database_utility.punish_user_with_wrong_answer(wrong_user)
                    await client_bot_handler.telebotConf.bot.send_message(chat_id=wrong_user.chat_id,
                                                                          text=OutPutMessages.you_gave_a_wrong_answer(
                                                                              question.request_word))
                    await update_pin_message(client_bot_handler, wrong_user.user_id, wrong_user.chat_id, None)
            else:
                pass

        await update_pin_message(client_bot_handler, user_id, call.message.chat.id,
                                 message_id=call.message.message_id)
