from constants import OutPutMessages
from exceptions import handle_my_exceptions
from handlers.profile_handler import update_pin_message


def handler_music(client_bot_handler):
    @client_bot_handler.telebotConf.bot.message_handler(commands=['gimme_music'])
    @handle_my_exceptions(client_bot_handler.telebotConf.bot)
    async def give_me_music(message):
        chat_id = message.chat.id

        if not client_bot_handler.database_utility.check_score_for_music(message.from_user.id):
            await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                  text=OutPutMessages.not_enough_credit_answer_question_to_get)
        else:
            select_channel = client_bot_handler.database_utility.get_user_selected_channel(chat_id)
            if not select_channel:
                await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                      text=OutPutMessages.select_one_of_channels)
            music_message = await client_bot_handler.my_client.select_a_music_randomly_with_best_local_score(
                select_channel)
            forwarded_music = await client_bot_handler.my_client.send_client_message_to_my_bot(music_message)
            await update_pin_message(client_bot_handler, message.from_user.id, chat_id)
            await client_bot_handler.telebotConf.bot.forward_message(chat_id=chat_id, message_id=forwarded_music.id,
                                                                     from_chat_id=forwarded_music.sender.id)
