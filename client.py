import os
import json
import aiohttp
import requests
import websockets


class Client:
    BASE_URL = os.getenv('API_URL')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.session = None
        self.websocket = None
        self.auth()

    def auth(self):
        data = {"email": self.email, "password": self.password}
        # checking for correct auth data
        response = requests.post("http://" + Client.BASE_URL + "/api/auth/", json=data)
        if response.status_code == 200:
            self.token = json.loads(response.text)['token']
            headers = {"Authorization": f"Token {self.token}"}
            self.session = aiohttp.ClientSession("http://" + Client.BASE_URL, headers=headers)

    async def upload_file(self, file_path):
        file = open(file_path + ".jpg", 'rb')
        async with self.session.post("/api/files/upload", data={'file': file}) as resp:
            file.close()
            if resp.status == 200:
                os.remove(file_path + ".jpg")
                return json.loads(await resp.text())['id']

    async def connect_websocket(self):
        self.websocket = await websockets.connect(f"ws://{Client.BASE_URL}/ws/chat/{self.token}/", open_timeout=None)

    async def start(self):
        await self.connect_websocket()