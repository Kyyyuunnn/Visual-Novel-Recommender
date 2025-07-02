import asyncio
import httpx
import readchar

from fetch_tags import fetch_top10_tags

async def recommend(token: str, top_tags: dict, page: int = 0, results_per_page: int = 10) -> list:
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    url = "https://api.vndb.org/kana/vn"

    tag_filters = [
        ["tag", "=", [tag_id, 0, 1.0]] for tag_id in top_tags.keys()
    ]

    query = {
        "filters": ["or"] + tag_filters,
        "fields": "id, title, rating",
        "sort": "rating",
        "reverse": True,
        "results": results_per_page,
        "page": page + 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=query)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []

async def pipeline(token: str, vn_titles: list[str], results_per_page: int = 10):
    top_10_titles = vn_titles[:10]
    top_tags = await fetch_top10_tags(token, top_10_titles)
    read_titles_set = set(vn_titles)

    page = 0


    while True:
        recommendations = await recommend(token, top_tags, page=page, results_per_page=results_per_page)

        filtered_recommendations = [vn for vn in recommendations if vn.get("title") not in read_titles_set]

        print(f"\n--- Page {page + 1} ---")
        if filtered_recommendations:
            for vn in filtered_recommendations:
                print(f"- {vn.get('title')} (Rating: {vn.get('rating')})")
        else:
            print("No recommendations found on this page.")

        print("\nPress → for next page, ← for previous page, or q to quit.")
        key = readchar.readkey()

        if key == readchar.key.RIGHT:
            page += 1
        elif key == readchar.key.LEFT:
            if page > 0:
                page -= 1
            else:
                print("Already at the first page.")
        elif key.lower() == 'q':
            print("Exiting recommendations.")
            break
        else:
            print("Invalid input. Use ←, →, or q.")