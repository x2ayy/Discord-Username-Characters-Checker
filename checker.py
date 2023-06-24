from random import sample as rand_sample
from string import ascii_letters
from requests import patch as req_patch
from time import sleep
from colorama import Fore


BASE_URL = "https://discord.com/api/v9/users/@me"

REQUEST_HEADERS = {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization":"YOUR-TOKEN-GOES-HERE"
}


def generate_random_username(length: int) -> str:
    return ''.join(rand_sample(ascii_letters, length))

def check_username(user: str):
    if 1 > len(user) < 33:
        print("Username must be 2-32 Characters")
        return
    
    user = user.lower()
        
    data = {
        "username": user
    }
    check = req_patch(BASE_URL, headers=REQUEST_HEADERS, json=data)
    checked_user = check.json()
    try:
        if checked_user["errors"]["username"]["_errors"][0]["code"] == "USERNAME_ALREADY_TAKEN":
            print(f"{Fore.RED}[+] {user} is not available {Fore.RESET}")
    except KeyError:
        try:
            if checked_user["errors"]["password"]:
                print(f"{Fore.GREEN}[+] {user} is available {Fore.RESET}")
        except KeyError:
            if check.status_code == 403 or check.status_code == 401:
                print(f"{Fore.RED}[-] Your request was denied, you need to have the name change option available for it to work! {Fore.RESET}")

def main_menu() -> list:
    print("Welcome to Discord Username Checker")
    flag = False
    while flag is False:
        try:
            user_length = int(input("How many letters in the username?  >"))
            how_many_to_check_for = int(input("How many random usernames do you want to check? >"))
            flag = True
        except ValueError:
            print("Please enter a length of the letters and how many times as a whole number\n\
                  Example: 2 for 2 letter usernames, 100 if you want to check 100 random usernames")
    return [user_length, how_many_to_check_for]


if __name__ == "__main__":
    username_letters, check_range = main_menu()

    for i in range(check_range):
        user = generate_random_username(username_letters)
        check_username(user)
        # Change this to your needs as no proxy support your requests will be blocked if spamming a lot so i recommend not putting too low
        sleep(0.8)
        
