from TGConvertor.manager import SessionManager
from pathlib import Path
import asyncio

session_file = '/src/tg_accounts/tg_accounts/48663657826.session'


async def get_session_string(path):
    session = await SessionManager.from_telethon_file(path)
    res = session.to_pyrogram_string()
    return res
