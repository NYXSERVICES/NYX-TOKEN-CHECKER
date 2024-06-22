import os
import sys
import time
import asyncio
import threading
import requests
import ctypes
import secrets
import string
from colorama import Fore, Style, init
from datetime import datetime
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System

init()
current_time = datetime.now().strftime("%H:%M:%S")
start_time = time.time()
lp = "\033[38;2;197;134;255m"
w = "\033[1;37m"
r = "\033[0;31m"

num_generated_tokens = 0  # Variable to track the number of generated tokens

def update_title(num_tokens):
    while True:
        elapsed_time = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        ctypes.windll.kernel32.SetConsoleTitleW(f" {hours:02d}:{minutes:02d}:{seconds:02d} | NYX SERVICES | NYX CHECKER | https://discord.gg/8Z2r9qjdCr | FOUND {num_tokens} TOKENS | Generated: {num_generated_tokens}")
        time.sleep(1)

async def loading(num_tokens):
    os.system('cls' if os.name == 'nt' else 'clear')
    ctypes.windll.kernel32.SetConsoleTitleW("Loading...")
    print("Loading", end="", flush=True)
    for i in range(3):
        print(".", end="", flush=True)
        await asyncio.sleep(1)
    print()
    os.system('cls' if os.name == 'nt' else 'clear')
    threading.Thread(target=update_title, args=(num_tokens,)).start()
    await art(num_tokens)

def load_tokens():
    if os.path.exists('data/tokens.txt'):
        with open('data/tokens.txt', 'r') as file:
            tokens = [line.strip() for line in file.readlines()]
            return tokens, len(tokens)
    return [], 0

def generate_tokens(num_tokens):
    global num_generated_tokens
    with open('data/tokens.txt', 'w') as file:
        for _ in range(num_tokens):
            token = ''.join(secrets.choice(string.ascii_letters + string.digits + '_') for _ in range(59))
            file.write(token + "\n")
            num_generated_tokens += 1  # Increment the count of generated tokens

async def check_token(num_tokens):
    valid_tokens = []
    invalid_tokens = []
    tokens, _ = load_tokens()
    for token in tokens:
        headers = {'Content-Type': 'application/json', 'authorization': token}
        url = "https://discordapp.com/api/v9/users/@me"
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            valid_tokens.append(token)
            user_data = r.json()
            username = user_data['username']
            discriminator = user_data['discriminator']
            user_id = user_data['id']
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}.png" if user_data['avatar'] else "No Avatar"
            nitro_status = "Yes" if user_data['premium_type'] == 1 else "No"
            twofa_status = "Yes" if user_data['mfa_enabled'] else "No"
            phone_status = "Yes" if user_data.get('phone', None) else "No"
            email_status = "Verified" if user_data.get('verified', False) else "Not Verified"
            locale = user_data.get('locale', 'Unknown')
            flags = user_data.get('flags', 'None')

            # Additional information that Discord API provides
            if 'email' in user_data:
                email = user_data['email']
            else:
                email = "Not available"

            if 'phone' in user_data:
                phone = user_data['phone']
            else:
                phone = "Not available"

            if 'bio' in user_data:
                bio = user_data['bio']
            else:
                bio = "Not available"

            print(Colorate.Vertical(Colors.purple_to_blue, f"[+] {token} is working!\nUsername: {username}#{discriminator}\nUser ID: {user_id}\nAvatar URL: {avatar_url}\nNitro: {nitro_status}\n2FA: {twofa_status}\nPhone: {phone_status}\nEmail: {email}\nBio: {bio}\nLocale: {locale}\nFlags: {flags}"))
        else:
            invalid_tokens.append(token)
            print(Colorate.Vertical(Colors.purple_to_red, f"[-] {token} is not working"))

    # Write valid and invalid tokens to files
    with open('data/valid.txt', 'a') as valid_file, open('data/invalid.txt', 'a') as invalid_file:
        valid_file.write("\n".join(valid_tokens) + "\n")
        invalid_file.write("\n".join(invalid_tokens) + "\n")

    # Update tokens.txt to remove invalid tokens
    with open('data/tokens.txt', 'w') as tokens_file:
        tokens_file.write("\n".join(valid_tokens))

async def art(num_tokens):
    logo = (Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(f''' 
                                  _   ___   ____   __
                                  | \ | \ \ / /\ \ / /  https://discord.gg/8Z2r9qjdCr
                                  |  \| |\ V /  \ V /   NYX SERVICES | nyx checker
                                  |     | \ /   /   \   Tokens available | ({num_tokens})
                                  | |\  | | |  / /^\ \\ Version | v0.5
                                  \_| \_/ \_/  \/   \/
''')))
    print(logo)

async def redo(num_tokens):
    await art(num_tokens)

async def main():
    global num_generated_tokens  # Use global variable to keep track of generated tokens count
    tokens, num_tokens = load_tokens()
    await loading(num_tokens)
    print(f"""
    {lp}[{w}1{r}{lp}]{r} {w}Check tokens{r}
    {lp}[{w}2{r}{lp}]{r} {w}Generate tokens{r}
    {lp}[{w}3{r}{lp}]{r} {w}Exit{r}
    """)
    choice = input(Colorate.Vertical(Colors.purple_to_blue, "  ╼"))
    if choice == "1":
        await check_token(num_tokens)
        input("Press Enter to continue...")
        await asyncio.sleep(2)
        await main()
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    elif choice == "2":
        num_to_generate = int(input("Enter number of tokens to generate: "))
        generate_tokens(num_to_generate)
        print(f"Generated {num_to_generate} tokens.")
        input("Press Enter to continue...")
        await asyncio.sleep(2)
        await main()
    else:
        print(Colorate.Vertical(Colors.purple_to_red, "Found error please choose a valid number"))
        print(Colorate.Vertical(Colors.purple_to_red, "redirecting..."))
        time.sleep(0.9)
        await loading(num_tokens)

asyncio.run(main())
