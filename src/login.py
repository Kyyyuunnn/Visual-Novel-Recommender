import asyncio
from azaka import Client

async def login_and_greet(token: str):
    try:
        async with Client(token=token) as client:
            auth_info = await client.get_auth_info()
            username = auth_info.username

            # using token for user greeting
            user_list = await client.get_user(username)
            if user_list: # checks if true or false
                print(f"Login successful! Welcome {user_list[0].username}!")
            else: 
                print("Login successful, but unable to find user info.")
    except Exception as e:
        print("Login failed: ", e)

def login(token: str):
    asyncio.run(login_and_greet(token))