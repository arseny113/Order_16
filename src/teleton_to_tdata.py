from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio

from TGConvertor.manager import SessionManager
from TGConvertor import TeleSession
import os

async def converter(path):
    # Load the client from telethon.session file
    # We don't need to specify api, api_id or api_hash, it will use TelegramDesktop API by default.
    client = TelegramClient(path)

    # flag=UseCurrentSession
    #
    # Convert Telethon to TDesktop using the current session.
    tdesk = await client.ToTDesktop(flag=UseCurrentSession)

    # Save the session to a folder named "tdata"
    tdesk.SaveTData(f"{path[:-20]}/tdata")
    
