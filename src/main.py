import os
import asyncio
from login import login, auto_login, logout
from manual_search import manual_search, vn_search
from fetch_user_list import fetch_user_list, read_saved_user_info

def main():
    info_file = "info.txt"

    token = None
    username = None

    if os.path.exists(info_file):
        with open(info_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("token="):
                    token = line.strip().split("=", 1)[1]
                elif line.startswith("username="):
                    username = line.strip().split("=", 1)[1]

    if username:
        print(f"Welcome Back {username}! ")
    else:
        print(f"Welcome to VNReccommender! ")
    
    print(f"Please choose an option below. ")

    print("1: Login (please go through this option at least once before beginning to use the application.) ")
    print("2: Manually input novels")
    print("3: Import your VNDB read list")
    print("4: Import another user's list")
    print("5: Logout")

    choice = input("Enter your choice (1-5): ").strip()

    # placeholder functions
    if choice == "1":
        token = input("Please enter your VNDB API token: ").strip()
        login(token)
        username, token = read_saved_user_info()
    elif choice == "2": 
        if token:
            asyncio.run(manual_search(token))
        else:
            print("You must login first.")
    elif choice == "3":
        if username and token:
            fetch_user_list(username, token)
        else:
            print("You must login first before importing your list.")
    elif choice == "4":
        if token:
            other_user_id = input("Input the user's ID you'd like to import (e.g. u123456): ").strip()
            fetch_user_list(other_user_id, token)
        else:
            print("You must login first before importing another user's list.")
    elif choice == "5":
        logout()
    else:
        print("Invalid option ")

# for main to exe
if __name__ == "__main__":
    main()
