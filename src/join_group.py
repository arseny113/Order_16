import asyncio

from pyrogram import Client

from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatAction, MessageMediaType
from pyrogram.handlers import MessageHandler

from typing import AsyncGenerator

from TGConvertor.manager import SessionManager

from teleton_to_tdata import converter

import os
import json

import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"



tg_accounts = {}
apps = []
path_accounts = 'tg_accounts'
path_parser_account = 'parser_account'
path_proxy = 'proxy'
name_target_group = 'Название целевого чата'
name_copy_group = 'test_copy_order' # Этот чат нужен только для реализации парсинга, вы можете выйти из него, как только добавите в него все аккаунты
accounts = os.listdir(path_accounts)
parser_files = os.listdir(path_parser_account)
users = []
copy_ids = []
convert_ids = {}
original_messages_ids = []
group_link = "Test_damn_target_chat"

async def get_session_string(path):
    session = await SessionManager.from_telethon_file(path)
    res = session.to_pyrogram_string()
    return res

async def main():
    for account in accounts:
        data = json.load(open(f'{path_accounts}/{account}/tdata/{account}.json'))
        #proxy_data= json.load(open(f'{path_proxy}/{account}.json'))
        """proxy = {'scheme': proxy_data['scheme'],
                 'hostname': proxy_data['hostname'],
                 'port': proxy_data['pord'],
                 'username': proxy_data['username'],
                 'password': proxy_data['password']}"""
        session = await get_session_string(f'{path_accounts}/{account}/tdata/{account}.session')
        tg_accounts[account] = [data['app_id'], data['app_hash'], session]
        apps.append(Client(name=account, api_id=tg_accounts[account][0], api_hash=tg_accounts[account][1], session_string=session, ))#proxy=proxy # ,api_id=tg_accounts[account][0], api_hash=tg_accounts[account][1],
        try:
            tdata = os.listdir(f'{path_accounts}/{account}/tdata')
        except:
            await converter(f'{path_accounts}/{account}/tdata/{account}.session')
    for i in range(len(apps)):
        try:
            await apps[i].start()
            print(apps[i].name, 'запущен')
        except:
            print(f'Аккаунт {apps[i].name} заблокирован')




if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

