import asyncio
import os
import re
from typing import List
from azaka import Client, Node, select
from azaka.paginator import Paginator

async def import_user_list(token: str, creds_file: str = "info.txt", output_file: str = "user_list.txt"):

    # grabbing u#
    if not os.path.exists(creds_file):
        raise FileNotFoundError(f"Please login! {creds_file} missing.")
    with open(creds_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"user_id=(u\d+)", content)
    user_id_str = match.group(1)
    user_id = int(user_id_str.lstrip("u"))

    # building the query
    query = {
        "user": user_id,
        "fields": "id, finished, vn.title",
        "filters": ["finished", "!=", None],
        "sort": "finished",
        "reverse": True,
        "results": 25 #for now, will change later on, to help with bigger lists
    }


