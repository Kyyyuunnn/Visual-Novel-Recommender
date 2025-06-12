# import httpx

# # token (WILL REPLACE THIS LATER ON FOR USER TO INPUT THEMSELVES)
# vndb_token = "dummy token"

# def search (title):
#     url = "https://api.vndb.org/kana"
#     headers = {
#         "Authorization": f"token {vndb_token}"
#     }
#     payload = {
#         "filters": ["search", "=", title],
#         "fields": ["id", "title", "released"],
#         "sort": "search",
#         "results": 10
#     }

#     # checks responeses

#     try:
#         response = httpx.post(url, json = payload, timeout = 10)
#         response.raise_for_status()
#         return response.json().get("results", [])
#     except httpx.HTTPError as e:
#         print(f"Error with API: {e}")
#         return []
