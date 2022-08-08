import re

import telebot

from constants import OutPutMessages, Commands
from exceptions import _MyExceptions
from telegram_client import MusicChannelForResearchClient


async def update_pin_message(client_bot_handler, user_id, chat_id, message_id=None):
    user = client_bot_handler.database_utility.get_user(user_id)
    state_text = OutPutMessages.state_pinned_message(user.introducer_username, user.selected_channel, user.score)

    if message_id:
        await client_bot_handler.telebotConf.bot.edit_message_text(text=state_text,
                                                                   chat_id=chat_id, message_id=message_id)
        await client_bot_handler.telebotConf.bot.pin_chat_message(chat_id=chat_id, message_id=message_id)
    else:
        # prev_message = (await client_bot_handler.telebotConf.bot.get_chat(chat_id)).pinned_message
        # if prev_message:
        #     try:
        #         message = await client_bot_handler.telebotConf.bot.edit_message_text(state_text, user_id,
        #                                                                              message_id=prev_message.id)
        #         await client_bot_handler.telebotConf.bot.pin_chat_message(chat_id, message.id)
        #     except Exception as e:
        #         print(e)
        #         message = await client_bot_handler.telebotConf.bot.send_message(text=state_text, chat_id=chat_id)
        #         await client_bot_handler.telebotConf.bot.pin_chat_message(chat_id, message.id)
        # else:
        message = await client_bot_handler.telebotConf.bot.send_message(text=state_text, chat_id=chat_id)
        await client_bot_handler.telebotConf.bot.pin_chat_message(chat_id, message.id)


def handler_profile(client_bot_handler):
    @client_bot_handler.telebotConf.bot.message_handler(commands=[Commands.start])
    async def start_message(message):
        chat_id = message.chat.id
        user = client_bot_handler.database_utility.register_user(message.from_user, chat_id)
        if user.introducer_username:
            sent_message = await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                                 text=OutPutMessages.start_message())
            await update_pin_message(client_bot_handler, message.from_user.id, sent_message.chat.id, sent_message.id)
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text=OutPutMessages.set_introducer_button + "؟",
                                                          callback_data=f'set_introducer'))
            await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message(),
                                                                  reply_markup=markup)

    @client_bot_handler.telebotConf.bot.message_handler(commands=[Commands.about_us])
    async def about_us_message(message):
        chat_id = message.chat.id
        await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)

    @client_bot_handler.telebotConf.bot.callback_query_handler(func=lambda call: call.data == "set_introducer")
    async def on_introducer_button_tap(call):
        user_id = call.from_user.id
        force_reply = telebot.types.ForceReply(selective=False)
        await client_bot_handler.telebotConf.bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        await client_bot_handler.telebotConf.bot.send_message(chat_id=user_id,
                                                              text=OutPutMessages.send_introducer_user_name,
                                                              reply_markup=force_reply)

    @client_bot_handler.telebotConf.bot.message_handler(content_types=['text'], chat_types=['private'], regexp=r'@.*')
    async def handle_introducer_username(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        text: str = message.text
        if re.match(r'@[A-Za-z_]*', text):
            try:
                introducer = client_bot_handler.database_utility.set_introducer_first_time(user_id, text[1:])
                await client_bot_handler.telebotConf.bot.send_message(chat_id=introducer.chat_id,
                                                                      text=OutPutMessages.you_have_introduced_a_user)

                await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                      text=OutPutMessages.introducer_has_been_set(text))
                await update_pin_message(client_bot_handler, introducer.user_id, introducer.chat_id)
                await update_pin_message(client_bot_handler, user_id, message.chat.id)
            except _MyExceptions as e:
                await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                      text=e.message)

        else:
            await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                                  text=OutPutMessages.wrong_format_for_username)

    @client_bot_handler.telebotConf.bot.message_handler(commands=[Commands.show_channels])
    async def show_channel_list(message):
        chat_id = message.chat.id
        channels = MusicChannelForResearchClient.telegram_music_channels
        markup = telebot.types.InlineKeyboardMarkup()
        for ch in channels:
            markup.add(telebot.types.InlineKeyboardButton(text=ch, callback_data=f'select_channel_{ch}'))
        await client_bot_handler.telebotConf.bot.send_message(chat_id=chat_id,
                                                              text=OutPutMessages.use_score_to_get_music(channels),
                                                              reply_markup=markup)

    def select_channel_func_condition(call):
        c = call.data.startswith("select_channel_")
        c = c and call.data[15:] in MusicChannelForResearchClient.telegram_music_channels
        return c

    @client_bot_handler.telebotConf.bot.callback_query_handler(func=select_channel_func_condition)
    async def update_channel_for_user(call):
        await client_bot_handler.telebotConf.bot.edit_message_reply_markup(call.from_user.id,
                                                                           message_id=call.message.message_id,
                                                                           reply_markup=None)
        selected_channel = call.data[15:]
        client_bot_handler.database_utility.change_user_channel(call.from_user.id, selected_channel)
        musics = await client_bot_handler.my_client.get_channel_all_music_counts(selected_channel)
        await client_bot_handler.telebotConf.bot.edit_message_text(
            OutPutMessages.good_choice_music_condition(selected_channel, musics),
            call.from_user.id, message_id=call.message.message_id)
        await update_pin_message(client_bot_handler, call.from_user.id, call.message.chat.id)
