from random import sample as rand_sample
from string import ascii_letters, digits
from requests import post as req_post
from time import sleep
from colorama import Fore

BASE_URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

REQUEST_HEADERS = {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization": "YOUR-TOKEN-GOES-HERE"
}


def generate_random_username(length: int) -> str:
    characters = ascii_letters + digits  # Include both letters and digits
    return ''.join(rand_sample(characters, length))


def check_username(user: str):
    if 1 > len(user) < 33:
        print("Username must be 2-32 Characters")
        return

    data = {
        "username": user
    }
    check = req_post(BASE_URL, headers=REQUEST_HEADERS, json=data)

    try:
        if check.json()["taken"] is not True:
            print(f"{Fore.GREEN}[+] {user} is available{Fore.RESET}")
        else:
            print(f"{Fore.RED}{check.status_code} {user} is not available {Fore.RESET}")
    except KeyError:
        if check.status_code == 403 or check.status_code == 401:
            print("REQUEST DENIED. Is the Discord token correct? Are you sending too many requests?")
            return False


def main_menu() -> list:
    print("Welcome to Discord Username Checker")
    flag = False
    while flag is False:
        try:
            user_length = int(input("How many characters in the username?  >"))
            how_many_to_check_for = int(input("How many random usernames do you want to check? >"))
            flag = True
        except ValueError:
            print("Please enter the length of the characters and the number of usernames to check as whole numbers.\n\
                  Example: 2 for 2 character usernames, 100 if you want to check 100 random usernames")
    return [user_length, how_many_to_check_for]


if __name__ == "__main__":
    username_characters, check_range = main_menu()

    for i in range(check_range):
        user = generate_random_username(username_characters)
        check_username(user)
        # Change this to your needs. As there is no proxy support, your requests may be blocked if spamming a lot, so I recommend not putting it too low.
        sleep(1.2)