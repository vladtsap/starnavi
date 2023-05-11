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
POST_IDS = []  # [post_id]


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


async def create_new_post(session, token, text) -> int:
    async with session.post(
            url=f'{BASE_URL}/post',
            headers={'Authorization': f'Bearer {token}'},
            json={'text': text}
    ) as response:
        if response.status == 201:
            data = await response.json()
            return data['id']
        else:
            raise Exception('Failed to create post')


async def like_post(session, token, post_id):
    async with session.post(
            url=f'{BASE_URL}/post/{post_id}/like',
            headers={'Authorization': f'Bearer {token}'},
    ) as response:
        if response.status != 201:
            raise Exception('Failed to like post')


async def main():
    print('Starting bot')
    session = aiohttp.ClientSession()

    # Create users
    for _ in range(NUMBER_OF_USERS):
        username, password = fake_data.user_name(), fake_data.password(16)
        await create_new_user(session, username, password)
        token = await obtain_jwt_token(session, username, password)
        USER_DATA[username] = token

    print('Users were created')

    # Create posts
    for token in USER_DATA.values():
        for _ in range(fake_data.random_int(1, MAX_POSTS_PER_USER)):
            post_id = await create_new_post(session, token, text=fake_data.sentence())
            POST_IDS.append(post_id)

    print('Posts were created')

    # Like posts
    for token in USER_DATA.values():
        liked_posts = fake_data.random_int(1, MAX_LIKES_PER_USER)
        for post_id in fake_data.random_elements(elements=POST_IDS, length=liked_posts, unique=True):
            await like_post(session, token, post_id)

    print('Posts were liked')

    await session.close()

    print('Bot has finished its work')


# Run the main coroutine
asyncio.run(main())
