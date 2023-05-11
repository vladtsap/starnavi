import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER'))
MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))

BASE_URL = 'http://localhost:8000'

fake_data = Faker()

USER_DATA = {}  # {username: JWT-token}


async def create_new_user(session, username, password):
    async with session.post(
            url=f'{BASE_URL}/sign-up',
            json={'username': username, 'password': password}
    ) as response:
        if response.status != 201:
            raise Exception('Failed to create user')


async def obtain_jwt_token(session, username, password) -> str:
    async with session.post(
            url=f'{BASE_URL}/token',
            json={'username': username, 'password': password}
    ) as response:
        if response.status == 200:
            data = await response.json()
            return data['access']
        else:
            raise Exception('Failed to obtain JWT token')


async def create_new_post(session, token):
    async with session.post(
            url=f'{BASE_URL}/post',
            headers={'Authorization': f'Bearer {token}'},
            json={'text': fake_data.sentence()}
    ) as response:
        if response.status == 201:
            data = await response.json()
            return data['id']
        else:
            raise Exception('Failed to create post')

async def main():
    session = aiohttp.ClientSession()

    # Create users
    for _ in range(NUMBER_OF_USERS):
        username, password = fake_data.user_name(), fake_data.password(16)
        await create_new_user(session, username, password)
        token = await obtain_jwt_token(session, username, password)
        USER_DATA[username] = token

    await session.close()


# Run the main coroutine
asyncio.run(main())
