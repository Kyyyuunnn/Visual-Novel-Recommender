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
                "fields": "tags.rating, tags.id, tags.category",
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
                if tag.get("category") != "cont":
                    continue
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

    max_score = max(info["score"] for info in tag_scores.values())
    max_score = max(info["count"] for info in tag_scores.values())

    weighted_tags = {}
    for tag_id, info in tag_scores.items():
        # calculations
        norm_score = info["score"] / max_score if max_score else 0
        norm_count = info["count"] / max_score if max_score else 0
        final_weight = (norm_score * 0.8) + (norm_count * 0.2)
        weighted_tags[tag_id] = {
            "score": info["score"],
            "count": info["count"],
            "weight": final_weight
        }

    top_20 = dict(sorted(weighted_tags.items(), key=lambda x: x[1]["weight"], reverse=True)[:20])

    return top_20

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
