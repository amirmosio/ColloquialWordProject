import telebot

from constants import OutPutMessages
from exceptions import handle_my_exceptions
from handlers.profile_handler import update_pin_message
from models import ColloquialQuestion


def handler_question(client_bot_handler):
    @client_bot_handler.telebotConf.bot.message_handler(commands=['question'])
    @handle_my_exceptions(client_bot_handler.telebotConf.bot)
    async def give_me_music(message):
        chat_id = message.chat.id
        q: ColloquialQuestion = client_bot_handler.database_utility.select_a_new_question_for_user(message.from_user.id)

        client_bot_handler.database_utility.check_if_question_is_done(q.id)

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
        if question.done:
            pass
        else:
            question = client_bot_handler.database_utility.check_question_update_done_with_final_answer(question_id)


        await update_pin_message(client_bot_handler, user_id, call.message.chat.id,
                                 message_id=call.message.message_id)

    # @self.bot.bot.message_handler(content_types=['text'], chat_types=['supergroup', 'group'])
    # def handle_group_text_message(message):
    #     chat_id = message.chat.id
    #     text = message.text
    #
    #     token, sim_words = self.bot.language_model_service.get_back_interesting_token_and_similar_words(text)
    #     if token:

    # def vote_done_condition(vote):
    #     # vote.options[0].text, vote.options[0].voter_count
    #     return vote.total_voter_count >= 1
    #
    # @client_bot_handler.telebotConf.bot.poll_answer_handler(func=vote_done_condition)
    # def handle_vote_submit(update, context):
    #     print(update)
