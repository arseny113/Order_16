import asyncio

from pyrogram import Client
from topyrogram import get_session_string
import os
import json


tg_accounts = {}
apps = []
accounts = os.listdir('C://Users/arsen/Order16/pythonProject2/src/tg_accounts')
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
                print('This account is blocked')

if __name__ == '__main__':
    asyncio.run(main())


