from login import login

def main():
    print(f"Welcome to VNReccommender! ")
    print(f"Please choose an option below. ")

    print("1: Login (please go through this option at least once before beginning to use the application.) ")
    print("2: Manually input novels (MUST LOGIN BEFORE USE)")
    print("3: Exit")

    choice = input("Enter your choice (1-3): ")

    # placeholder functions
    if choice == "1":
        token = input("Please enter your VNDB API token: ").strip()
        login(token)
    elif choice == "2": 
        manual()
    elif choice == "3":
        print("Goodbye! Enjoy Reading! ")
    else:
        print("Invalid option ")


# for main to exe
if __name__ == "__main__":
    main()
    
