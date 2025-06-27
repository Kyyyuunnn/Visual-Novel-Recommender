import asyncio
import httpx
import json
import os

async def fetch_top10_tags(token: str, vn_titles: list[str]) -> dict:
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    vn_url = "https://api.vndb.org/kana/vn"
    tag_scores = {}

    async with httpx.AsyncClient() as client:
        for title in vn_titles:
            json_data = {
                "filters": ["search", "=", title],
                "fields": "tags.rating, tags.id",
                "results": 1
            }

            response = await client.post(vn_url, headers=headers, json=json_data)
            if response.status_code != 200:
                continue

            data = response.json()
            if not data["results"]:
                continue

            tags = data["results"][0].get("tags", [])
            for tag in tags:
                tag_id = tag["id"]
                rating = tag.get("rating")
                if rating is not None:
                    if tag_id in tag_scores:
                        tag_scores[tag_id]["score"] += rating
                        tag_scores[tag_id]["count"] += 1
                    else:
                        tag_scores[tag_id] = {
                            "score": rating,
                            "count": 1
                        }

    for tag_id, info in tag_scores.items():
        info["score"] /= info["count"]

    top_10 = dict(sorted(tag_scores.items(), key=lambda x: x[1]["count"], reverse=True)[:10])

    return top_10

async def main_fetch_tags(token: str):
    input_file = "data/read_list.txt"
    output_file = "data/top_tags.json"

    if not os.path.exists(input_file):
        print("Read list not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        vn_titles = [line.strip() for line in f.readlines() if line.strip()]

    top_10_titles = vn_titles[:10]
    tag_data = await fetch_top10_tags(token, top_10_titles)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tag_data, f, indent=2)

    print(f"Saved top tags and ratings to {output_file}")
