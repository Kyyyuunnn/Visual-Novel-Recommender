import asyncio
import os
from azaka import Client, Node, select

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

async def vn_search(title: str, token: str):
    query = (
        select("title")
        .frm("vn")
        .where(Node("search") == title)
    )
    try:
        async with Client(token=token) as client:
            response = await client.execute(query=query)
            return [vn.title for vn in response.results]
    except Exception as e:
        print("Search failed:", e)
        return []

async def manual_search(token: str):
    saved_vn = []

    while True:
        title = input("Please enter the title of the visual novel you'd like to look up: ").strip()
        if not title:
            print("Title cannot be empty")
            continue

        results = await vn_search(title, token)

        if not results:
            print("No results found.")
        else:
            print("Search results:")
            for i, vn_title in enumerate(results):
                print(f"{i + 1}: {vn_title}")

            try:
                choice = int(input("Choose the visual novel you're looking for (or 0 to cancel): "))
                if 1 <= choice <= len(results):
                    selected_title = results[choice - 1]
                    saved_vn.append(selected_title)
                    print(f"Added '{selected_title}' to your list.")
                elif choice == 0:
                    print("Cancelled.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")

        cont = input("Would you like to add another title? (y or n): ").strip().lower()
        if cont != 'y':
            break

    output_path = os.path.join(DATA_DIR, "read_list.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        for vn in saved_vn:
            file.write(vn + "\n")

    print("\nSearch complete. Saved visual novels:")
    for vn in saved_vn:
        print(f"- {vn}")
    print(f"All novels have been saved to '{output_path}'.")
