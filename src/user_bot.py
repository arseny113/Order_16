import asyncio

from pyrogram import Client

from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatAction, MessageMediaType
from pyrogram.handlers import MessageHandler

from typing import AsyncGenerator

from TGConvertor.manager import SessionManager

import os
import json

import time



re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"



tg_accounts = {}
apps = []
accounts = os.listdir('C://Users/arsen/Order16/pythonProject2/src/tg_accounts')
parser_files = os.listdir('C://Users/arsen/Order16/pythonProject2/src/parser_account')
users = []
copy_ids = []
convert_ids = {}
original_messages_ids = []




async def get_session_string(path):
    session = await SessionManager.from_telethon_file(path)
    res = session.to_pyrogram_string()
    return res


async def get_ids(Client: Client, new_message: Message):
    convert_ids[f"{original_messages_ids[-1]}"] = new_message.id


async def main():
    for account in accounts:
        data = json.load(open(f'C://Users/arsen/Order16/pythonProject2/src/tg_accounts/{account}/{account}.json'))
        session = await get_session_string(f'C://Users/arsen/Order16/pythonProject2/src/tg_accounts/{account}/{account}.session')
        tg_accounts[account] = [data['app_id'], data['app_hash'], session]
        apps.append(Client(name=account,api_id=tg_accounts[account][0], api_hash=tg_accounts[account][1],session_string=tg_accounts[account][2]))
    for i in range(len(apps)):
        try:
            await apps[i].start()
        except:
            print(f'Аккаунт {apps[i].name} заблокирован')
    parser_data = json.load(open(f'C://Users/arsen/Order16/pythonProject2/src/parser_account/{parser_files[0]}/{parser_files[0]}.json'))
    parser_session = await get_session_string(f'C://Users/arsen/Order16/pythonProject2/src/parser_account/{parser_files[0]}/{parser_files[0]}.session')
    parser = Client(name=parser_data['phone'], api_id=parser_data['app_id'], api_hash=parser_data['app_hash'], session_string=parser_session)
    await parser.start()
    parser.add_handler(MessageHandler(get_ids))

    chats = []
    groups = []

    result = parser.get_dialogs()
    async for dialog in result:
        chats.append(dialog.chat)
    for chat in chats:
        try:
            if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
                if chat.title == 'test_target_chat':
                    group_for_parsing = chat
                if chat.title == 'Test_copy_chat_order':
                    group_for_copy = chat
                else:
                    groups.append(chat)
        except:
            continue
    print(gr + '[+] Выберите группу для парсинга :' + re)
    i = 0
    for g in groups:
        print(gr + '[' + cy + str(i) + gr + ']' + cy + ' - ' + g.title)
        i += 1
    print('')
    g_index = input(gr + "[+] Введите номер : " + re)
    target_group = groups[int(g_index)]
    messages_data: AsyncGenerator[Message, None] = parser.get_chat_history(chat_id=target_group.id)
    messages = []
    while True:
        start_id = int(input(gr + "[+] Введите id начального сообщения: " + re))
        finish_id = int(input(gr + "[+] Введите id конечного сообщения: " + re))
        async for message in messages_data:
            if start_id <= message.id <= finish_id:
                messages.append(message)
        if len(messages) != 0:
            break
        else:
            print(gr + "Ввод некорректен, поробуйте еще раз" + re)
    messages = list(reversed(messages))
    black_ids = [int(black_id.strip()) for black_id in input(gr + 'Введите список id сообщений, которые парсить не надо, через запятую:\n' + re).split(',')]
    list_of_users = list(set([message.from_user.id for message in messages]))
    copied_media_groups_ids = []
    if len(list_of_users) > len(accounts):
        print(re + 'У вас мало аккаунтов для того чтобы парсть эту группу, добавьте аккаунтов и попробуйте снова')
    for message in messages:
        user = message.from_user.id
        user_bot = apps[list_of_users.index(user)]
        if not message.service and message.id not in black_ids:
            media_group_id = message.media_group_id
            reply_message_id = message.reply_to_message_id
            original_messages_ids.append(message.id)
            try:
                if media_group_id not in copied_media_groups_ids:
                    await parser.copy_media_group(chat_id=group_for_copy.id, from_chat_id=target_group.id,
                                              message_id=message.id)
            except:
                await parser.copy_message(chat_id=group_for_copy.id, from_chat_id=target_group.id,message_id=message.id)
            messages_data: AsyncGenerator[Message, None] = parser.get_chat_history(chat_id=group_for_copy.id)
            copy_messages = [copy_message async for copy_message in messages_data if not copy_message.service]
            if copy_messages[0].text or copy_messages[0].media:
                if copy_messages[0].media:
                    media = copy_messages[0].media
                    if media == MessageMediaType.PHOTO:
                        await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.UPLOAD_PHOTO)
                        time.sleep(2)
                    if media == MessageMediaType.VIDEO:
                        await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.UPLOAD_VIDEO)
                        time.sleep(4)
                    if media == MessageMediaType.VIDEO_NOTE:
                        await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.RECORD_VIDEO_NOTE)
                        time.sleep(message.video_note.duration)
                    if media == MessageMediaType.VOICE:
                        await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.RECORD_AUDIO)
                        time.sleep(message.voice.duration)
                    if media == MessageMediaType.STICKER:
                        await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.CHOOSE_STICKER)
                        time.sleep(1)
                else:
                    await user_bot.send_chat_action(chat_id=group_for_parsing.id, action=ChatAction.TYPING)
                    time.sleep(len(message.text) / 4.4)

            try:
                if media_group_id not in copied_media_groups_ids:
                    if reply_message_id:
                        await user_bot.copy_media_group(chat_id=group_for_parsing.id, from_chat_id=group_for_copy.id,
                                                        message_id=copy_messages[0].id,
                                                        reply_to_message_id=convert_ids[f"{reply_message_id}"]
                                                        )
                    else:
                        await user_bot.copy_media_group(chat_id=group_for_parsing.id, from_chat_id=group_for_copy.id,
                                                        message_id=copy_messages[0].id,
                                                        )

                    copied_media_groups_ids.append(media_group_id)
            except:
                if reply_message_id:
                    await user_bot.copy_message(chat_id=group_for_parsing.id, from_chat_id=group_for_copy.id,
                                                message_id=copy_messages[0].id,
                                                reply_to_message_id=convert_ids[f"{reply_message_id}"])
                else:
                    await user_bot.copy_message(chat_id=group_for_parsing.id, from_chat_id=group_for_copy.id,
                                                message_id=copy_messages[0].id,
                                                )
            time.sleep(0.6)
            try:
                await parser.delete_messages(chat_id=group_for_copy.id, message_ids=copy_messages[0].id)
            except:
                pass


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())