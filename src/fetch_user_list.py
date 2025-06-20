import asyncio
import os
import re
from typing import List
from azaka import Client, Node, select
from azaka.paginator import Paginator

async def import_user_list(token: str, user_id: str = None, creds_file: str = "info.txt", output_file: str = "user_list.txt", max_results: int = 25):

    # reading for u#
    if not os.path.exists(creds_file):
        raise FileNotFoundError(f"Please login! {creds_file} missing.")
    with open(creds_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"user_id=(u\d+)", content)
    return match.group(1)

