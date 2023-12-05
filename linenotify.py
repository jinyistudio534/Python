import json
from requests import Response
import datetime
import os
import asyncio
from functools import partial

import aiohttp
from typing import List

NOTIFY_URL = 'https://notify-api.line.me/api/notify'
NOTIFY_STATUS_URL = 'https://notify-api.line.me/api/status'

# LINEのgetリクエストを行う
async def line_get_request(url: str, token: str) -> json:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url = url,
            headers = {'Authorization': 'Bearer ' + token}
        ) as resp:
            return await resp.json()

# LINEのpostリクエストを行う
async def line_post_request(url: str, headers: dict, data: dict) -> json:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url = url,
            headers = headers,
            data = data
        ) as resp:
            return await resp.json()


class LineNotify:
        def __init__(self, notify_token: str) -> None:
                self.notify_token = notify_token                
                self.loop = asyncio.get_event_loop()

        # LINE Notifyでテキストメッセージを送信
        async def push_message_notify(self, message: str) -> json:
                data = {'message': f'message: {message}'}
                return await line_post_request(
                url = NOTIFY_URL, 
                headers = {'Authorization': f'Bearer {self.notify_token}'}, 
                data = data
                )

        # LINE Notifyで画像を送信
        async def push_image_notify(self, message: str, image_url: str) -> dict:
                if len(message) == 0:
                        message = "画像を送信しました。"

                data = {
                        'imageThumbnail': f'{image_url}',
                        'imageFullsize': f'{image_url}',
                        'message': f'{message}',
                }
                return await line_post_request(
                        url = NOTIFY_URL, 
                        headers = {'Authorization': f'Bearer {self.notify_token}'}, 
                        data = data
                )

        # LINE Notifyのステータスを取得
        async def notify_status(self) -> Response:
                async with aiohttp.ClientSession() as session:
                        async with session.get(
                                url = NOTIFY_STATUS_URL,
                                headers = {'Authorization': 'Bearer ' + self.notify_token}
                        ) as resp:
                                return resp

        # LINE Notifyの1時間当たりの上限を取得
        async def rate_limit(self) -> int:
                resp = await self.notify_status()
                ratelimit = resp.headers.get('X-RateLimit-Limit')
                return int(ratelimit)

        # LINE Notifyの1時間当たりの残りの回数を取得
        async def rate_remaining(self) -> int:
                resp = await self.notify_status()
                ratelimit = resp.headers.get('X-RateLimit-Remaining')
                return int(ratelimit)

        # LINE Notifyの1時間当たりの画像送信上限を取得
        async def rate_image_limit(self) -> int:
                resp = await self.notify_status()
                ratelimit = resp.headers.get('X-RateLimit-ImageLimit')
                return int(ratelimit)

        # LINE Notifyの1時間当たりの残り画像送信上限を取得
        async def rate_image_remaining(self) -> int:
                resp = await self.notify_status()
                ratelimit = resp.headers.get('X-RateLimit-ImageRemaining')
                return int(ratelimit)
        
line = LineNotify('your token')
asyncio.run(line.push_message_notify("hello 123"))


