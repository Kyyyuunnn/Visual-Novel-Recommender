import asyncio
import os
from azaka import Client

def read_saved_user_info():
    info_file = "data/info.txt"
    token = None
    username = None
    if os.path.exists(info_file):
        with open(info_file, "r") as f:
            for line in f:
                if line.startswith("token="):
                    token = line.strip().split("=", 1)[1]
                elif line.startswith("username="):
                    username = line.strip().split("=", 1)[1]
    return username, token

info_file = "data/info.txt"

async def login_and_greet(token: str):
    try:
        async with Client(token=token) as client:
            auth_info = await client.get_auth_info()
            username = auth_info.username
            user_id = auth_info.id  # grabs id

            # saves token
            os.makedirs("data", exist_ok=True)
            with open(info_file, "w") as f:
                f.write(f"token={token}\nusername={username}\nuser_id={user_id}")

            print(f"Login successful! Welcome {username}!")

    except Exception as e:
        print("Login failed: ", e)

def login(token: str):
    asyncio.run(login_and_greet(token))

def auto_login():
    if os.path.exists(info_file):
        try:
            with open(info_file, "r") as f:
                lines = f.read().splitlines()
                token = next(line.split("=")[1] for line in lines if line.startswith("token="))
            login(token)
            return True
        except Exception as e:
            print("Auto login failed:", e)
            return False
    else: 
        return False

def logout():
    if os.path.exists(info_file):
        os.remove(info_file)
        print("Logged out successfully.")
    else:
        print("You are not logged in.")
