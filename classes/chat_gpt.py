import os

import aiofiles
import httpx
from openai import AsyncOpenAI

from enum import Enum


# class ChatModel(Enum):
#     TEXT_GPT = 'gpt-3.5-turbo'


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self._ai_token = os.getenv('AI_TOKEN')
        self._proxy = os.getenv('PROXY')
        self._client = self._create_client()

    def _create_client(self):
        ai_client = AsyncOpenAI(
            api_key=self._ai_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
        )
        return ai_client

    @staticmethod
    async def _read_prompt(path: str) -> str:
        async with aiofiles.open(os.path.join('prompts', path), 'r', encoding='UTF-8') as file:
            prompt = await file.read()
        return prompt

    async def text_request(self, messages: list[dict[str, str]], prompt: str):
        message_list = [
                           {'role': 'system',
                            'content': await self._read_prompt(prompt)},
                       ] + messages
        completion = await self._client.chat.completions.create(
            messages=message_list,
            model="gpt-3.5-turbo",
        )
        response = completion.choices[0].message.content
        return response
