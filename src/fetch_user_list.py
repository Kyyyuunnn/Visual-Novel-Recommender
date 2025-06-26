# need to create a way to do more than 100 results

import asyncio
import httpx
import os

async def import_user_list(token: str, user_id: str, output_file: str = "read_list.txt"):
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, output_file)

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    url = "https://api.vndb.org/kana/ulist"

    all_titles = []
    page = 1
    batch_size = 100

    async with httpx.AsyncClient() as client:
        while True:
            json_data = {
                "user": user_id,
                "fields": "id,vote,vn.title",
                "filters": ["label", "=", 7],
                "sort": "vote",
                "reverse": True,
                "results": batch_size,
                "page": page
            }
            response = await client.post(url, headers=headers, json=json_data)
            if response.status_code != 200:
                print(f"Failed to fetch user list at page {page}: {response.text}")
                break

            data = response.json()
            results = data.get("results", [])
            if not results:
                break

            for entry in results:
                all_titles.append(entry["vn"]["title"])


            if len(results) < batch_size:
                break

            page += 1

    with open(output_path, "w", encoding="utf-8") as f:
        for title in all_titles:
            f.write(title + "\n")

    if all_titles:
        with open(output_path, "w",encoding="utf=8") as f:
            for title in all_titles:
                f.write(title + "\n")
            print("List has been imported! ")
    else:
        print("Nothing has been imported, please reenter the u#. ")
