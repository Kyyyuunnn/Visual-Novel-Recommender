import asyncio
from azaka import Client, select, Node

def read_saved_user_info():
    info_file = "info.txt"
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



def save_user_list(vns):
    with open("imported_user_list.txt", "w", encoding="utf-8") as file:
        for vn in vns:
            file.write(vn.title + "\n")

def fetch_user_list(user_id: str, token: str):
    async def _fetch():
        try:
            async with Client(token=token) as client:
                query = (
                    select("vn.title")
                    .frm("ulist")
                    .where(Node("user") == user_id)
                    .limit(100)
                )
                res = await client.execute(query=query)
                save_user_list(res.results)
                print(f"Imported {len(res.results)} visual novels into 'imported_user_list.txt'")
        except Exception as e:
            print("Failed to fetch user list:", e)

    asyncio.run(_fetch())
