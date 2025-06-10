import htppx

url = "https://api.vndb.org/kana"

def search (title: str, limit: int = 5):
    payload = {
        "filters": ["search", "=", title],
        "fields": ["id", "title", "released"],
        "results": limit
    }

    # checks responeses

    try:
        response = httpx.post(url, json = payload, timeout = 10)
        response.raise_for_status()
        return response.json().get("results", [])
    except httpx.HTTPError as e:
        print(f"Error with API: {e}")
        return []