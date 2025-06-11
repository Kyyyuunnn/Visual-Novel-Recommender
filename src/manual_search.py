from vndb_api import search

def manual():
    while True:
        title = input("Enter the visual novel title: or 'quit' to stop searching: ")
        if title.lower() == 'quit':
            break
        
        results = search(title)

        # if no results reprompt
        if not results:
            print("No results found")
            continue
        
        # search results
        print("Search Results: ")

        for i in vn in enumerate(results, start = 1):
            title = vn.get("title", "Unknown Title")
            release = vn.get("released", "Unknown")
            print(f"{i}. {vn.title} (Released: {release})")
    
