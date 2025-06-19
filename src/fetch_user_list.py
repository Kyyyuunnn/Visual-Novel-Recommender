import asyncio
from azaka import Client, select, Node, Paginator

def save_user_list(vns):
    with open("imported_user_list.txt", "w", encoding="utf-8") as file:
        for vn in vns:
            file.write(vn.title + "\n")

async def fetch_user_list(user_id: str, token: str):
    try:
        async with Client(token=token) as client:
            query = (
                select("vn.title")
                .frm("ulist")
                .where(Node("user") == user_id)
            )
            paginator = Paginator(client, query=query, max_results_per_page=100)

            all_vns = []
            async for page in paginator:
                all_vns.extend(page.results)

            save_user_list(all_vns)
            print(f"Imported {len(all_vns)} visual novels into 'imported_user_list.txt'")
    except Exception as e:
        print("Failed to fetch user list:", e)

# To call the function from sync code:
def fetch_user_list_sync(user_id: str, token: str):
    asyncio.run(fetch_user_list(user_id, token))
