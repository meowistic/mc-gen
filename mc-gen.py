# imagine skidding (please dont tho, it took a while to make this)

import requests
from colorama import init, Fore
import time
import itertools
import random
import os

init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_combination(combo, amt):
    return ''.join(random.choice(combo) for _ in range(amt))

def generate_combinations_list(n, cc, amt):
    return [generate_combination(cc, amt) for _ in range(n)]

if not os.path.exists("config.txt"):
    with open("config.txt", "w") as f:
        f.write("1000")

def read_settings():
    with open("config.txt", "r") as f:
        return f.read().strip()

def save_settings(settings):
    with open("config.txt", "w") as f:
        f.write(settings)

def display_settings(settings):
    options = [
        ("save available usernames to file", settings[0]),
        ("include numbers", settings[1]),
        ("start alphabetically", settings[2]),
        ("only use numbers", settings[3])
    ]
    for i, (desc, value) in enumerate(options, start=1):
        status = Fore.GREEN + 'true' + Fore.LIGHTCYAN_EX if value == "1" else Fore.RED + 'false' + Fore.LIGHTCYAN_EX
        print(f"[{i}] {desc} - {status}")

def toggle_setting(settings, index):
    new_value = '0' if settings[index] == '1' else '1'
    return settings[:index] + new_value + settings[index + 1:]

def users(combinations, save):
    for username in combinations:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        response = requests.get(url)
        time.sleep(1.2)
        if response.status_code == 200 or response.status_code == 204:
            print(Fore.RED + f"[-] Username {username} taken.")
        elif "Couldn't find any profile with name" in response.text:
            print(Fore.GREEN + f"[+] Username {username} available.")
            if save:
                with open("users.txt", "a") as f:
                    f.write(f"username: {username}\n")
        elif response.status_code == 429:
            print("[-] Ratelimited, waiting 5 seconds.")
            time.sleep(5)

print("initializing..")
clear()

def menu():
    z = input(Fore.LIGHTCYAN_EX + """
> discord: kvts
 ███▄ ▄███▓ ▄████▄       ▄████ ▓█████  ███▄    █ 
▓██▒▀█▀ ██▒▒██▀ ▀█      ██▒ ▀█▒▓█   ▀  ██ ▀█   █ 
▓██    ▓██░▒▓█    ▄    ▒██░▄▄▄░▒███   ▓██  ▀█ ██▒
▒██    ▒██ ▒▓▓▄ ▄██▒   ░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒
▒██▒   ░██▒▒ ▓███▀ ░   ░▒▓███▀▒░▒████▒▒██░   ▓██░
░ ▒░   ░  ░░ ░▒ ▒  ░    ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ 
░  ░      ░  ░  ▒        ░   ░  ░ ░  ░░ ░░   ░ ▒░
░      ░   ░           ░ ░   ░    ░      ░   ░ ░ 
       ░   ░ ░               ░    ░  ░         ░ 
           ░  
<press enter to start>
<press 1+enter to change options>
""")
    if z == "1":
        settings = read_settings()
        print("<type the appropriate number+enter to switch>\n----")
        display_settings(settings)
        choice = input(Fore.LIGHTCYAN_EX+"")
        if choice in ['1', '2', '3', '4']:
            index = int(choice) - 1
            settings = toggle_setting(settings, index)
            save_settings(settings)
            print("Settings updated.")
        else:
            print("Invalid choice, returning to menu...")
            time.sleep(2)
        clear()
        menu()
    else:
        amt = int(input(Fore.MAGENTA+"[!] enter symbol amount: "))
        settings = read_settings()
        save = settings[0] == '1'
        include_numbers = settings[1] == '1'
        start_alphabetically = settings[2] == '1'
        only_numbers = settings[3] == '1'

        if only_numbers:
            characters = '0123456789'
        elif include_numbers:
            characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
        else:
            characters = 'abcdefghijklmnopqrstuvwxyz'

        if start_alphabetically:
            combinations = list(itertools.product(characters, repeat=amt))
            combinations = [''.join(combo) for combo in combinations]
        else:
            combinations = generate_combinations_list(100000, characters, amt)

        users(combinations=combinations, save=save)

menu()
