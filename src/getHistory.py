from typing import AsyncGenerator
from pyrogram.types import Message

async def get_history(client, start_id: int, end_id: int, chat_id):
    await client.statrt()
    messages: AsyncGenerator[Message, None] = client.get_chat_history()