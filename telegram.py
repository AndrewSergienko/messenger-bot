import os
import re
import json
from client import Client
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto


api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


async def create_post(photo, client):
    file_id = await client.upload_file(photo)
    data = json.dumps({"type": "message", "text": "cats", "chat": 9, "files": [file_id]})
    await client.websocket.send(data)


tg_client = TelegramClient('anon', api_id, api_hash)
messenger_client = Client(email=email, password=password)


@tg_client.on(events.NewMessage)
async def new_message_event(event):
    if event.message.peer_id.channel_id == -1001731110771 and len(re.findall(r'https://t.me/', event.message.text)) == 0:
        if type(event.message.media) == MessageMediaPhoto:
            await event.message.download_media(file=f"media/{event.message.id}")
            await create_post(f"media/{event.message.id}", client=messenger_client)


tg_client.start()
tg_client.loop.create_task(messenger_client.start())
tg_client.run_until_disconnected()