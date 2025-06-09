def main():
    print(f"Welcome to VNReccommender! ")
    print(f"Please choose an option below. ")

    print("1: Login to VNDB and find personalized recommendations")
    print("2: Manually input novels")
    print("3: Exit")

    choice = input("Enter your choice (1-3): ")

    # placeholder functions
    if choice == "1":
        login()
    elif choice == "2": 
        manual()
    elif choice == "3":
        print("Goodbye! Enjoy Reading! ")
    else:
        print("Invalid option ")


def manual():
    print("not implemented yet...")

if __name__ == "__main__":
    main()
    
