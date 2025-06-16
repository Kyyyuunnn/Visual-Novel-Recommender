from login import login, auto_login, logout
from manual_search import manual_search, vn_search
import os
import asyncio

def main():
    info_file = "info.txt"

    if os.path.exists(info_file):
        with open(info_file, "r") as f:
            lines = f.readlines()
            token = None
            username = None
            for line in lines:
                if line.startswith("token="):
                    token = line.strip().split("=")[1]
                elif line.startswith("username="):
                    username = line.strip().split("=")[1]
        if username:
            print(f"Welcome Back {username}! ")
        else: 
            print(f"Welcome Back! ")
    else:
        print(f"Welcome to VNReccommender! ")
    
    print(f"Please choose an option below. ")

    print("1: Login (please go through this option at least once before beginning to use the application.) ")
    print("2: Manually input novels")
    print("3: Import from user list")
    print("4: Logout")

    choice = input("Enter your choice (1-4): ")

    # placeholder functions
    if choice == "1":
        token = input("Please enter your VNDB API token: ").strip()
        login(token)
    elif choice == "2": 
        asyncio.run(manual_search(token))
    elif choice == "3":
        break
    elif choice == "4":
        logout()
        #print("Goodbye! Enjoy reading! ")
    else:
        print("Invalid option ")


# for main to exe
if __name__ == "__main__":
    main()
    
