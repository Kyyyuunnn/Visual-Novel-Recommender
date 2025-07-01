import asyncio
import httpx

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

    start = page * results_per_page

    query = {
        "filters": ["or"] + tag_filters,
        "fields": "id, title, rating",
        "sort": "rating",
        "reverse": True,
        "results": results_per_page,
        "start": start
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=query)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []

async def pipeline(token: str, vn_titles: list[str], rec_count: int = 10):
    top_10_titles = vn_titles[:10]
    top_tags = await fetch_top10_tags(token, top_10_titles)
    recommendations = await recommend(token, top_tags, num_results=rec_count * 3)

    read_titles_set = set(vn_titles)
    filtered_recommendations = [vn for vn in recommendations if vn.get("title") not in read_titles_set]

    filtered_recommendations = filtered_recommendations[:rec_count]

    print("\nRecommended Visual Novels:")
    if filtered_recommendations:
        for vn in filtered_recommendations:
            print(f"- {vn.get('title')} (Rating: {vn.get('rating')})")
    else:
        print("No recommendations found.")

