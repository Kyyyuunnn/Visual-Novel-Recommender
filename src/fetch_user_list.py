import asyncio
import httpx

async def import_user_list(token: str, user_id: str, output_file: str = "read_list.txt"):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    url = "https://api.vndb.org/kana/ulist"

    json_data = {
        "user": user_id,
        "fields": "id,vote,vn.title",
        "filters": ["label", "=", 7],
        "sort": "vote",
        "reverse": True,
        "results": 100
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=json_data)
            if response.status_code != 200:
                print(f"Failed to fetch user list: {response.text}")
                return
            data = response.json()
            titles = [entry["vn"]["title"] for entry in data.get("results", [])]

            with open(output_file, "w", encoding="utf-8") as f:
                for title in titles:
                    f.write(title + "\n")

            print(f"Successfully imported {len(titles)} voted VN titles.")

        except Exception as e:
            print(f"An error occurred: {e}")
