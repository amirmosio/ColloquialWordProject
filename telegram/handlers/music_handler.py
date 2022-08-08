# from constants import OutPutMessages, Commands
# from exceptions import handle_my_exceptions
# from handlers.profile_handler import update_pin_message
#
#
# def handler_music(client_bot_handler):
#     @client_bot_handler.telebotConf.bot.message_handler(commands=[Commands.music])
#     @handle_my_exceptions(client_bot_handler.telebotConf.bot)
#     async def give_me_music(message):
#         chat_id = message.chat.id
#
#         if not client_bot_handler.database_utility.check_score_for_music(message.from_user.id):
#             await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
#                                                                   text=OutPutMessages.not_enough_credit_answer_question_to_get)
#         else:
#             select_channel = client_bot_handler.database_utility.get_user_selected_channel(chat_id)
#             if not select_channel:
#                 await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
#                                                                       text=OutPutMessages.select_one_of_channels)
#             else:
#                 music_message = await client_bot_handler.my_client.select_a_music_randomly_with_best_local_score(
#                     select_channel)
#                 new_message = music_message.message + f"\n{chat_id}-{message.from_user.id}"
#                 music_message.message = new_message
#                 music_message.text = new_message
#                 forwarded_music = await client_bot_handler.my_client.send_client_message_to_my_bot(music_message)
#
#     @client_bot_handler.telebotConf.bot.message_handler(content_types=['audio'], chat_types=['private'], )
#     async def handle_music_receive(message):
#         chat_id = message.chat.id
#         user_id = message.from_user.id
#         destination_chat_id, destination_user_id = message.caption.split("\n")[-1].split("-")
#         message.caption = "\n".join(message.caption.split("\n")[:-1])
#         message.json['caption'] = message.caption
#         client_bot_handler.database_utility.take_score_for_music(user_id)
#         await update_pin_message(client_bot_handler, destination_user_id, destination_chat_id)
#         await client_bot_handler.telebotConf.bot.copy_message(chat_id=destination_chat_id,
#                                                               message_id=message.id,
#                                                               from_chat_id=chat_id,
#                                                               caption=message.caption)
