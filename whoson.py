import subprocess
import argparse
import sys
import time
import configparser
from client import Client
from configuration import Configuration


def handle_args(args):
    configuration = Configuration()

    if args.username:
        configuration.username(args.username)
        print(f"Username set as {args.username}")
    if args.client_id:
        configuration.client_id(args.client_id)
        print("Client ID set")
    if args.client_secret:
        configuration.client_secret(args.client_secret)
        print("Client secret set")
    
    if args.program:
        run(args, configuration)

def run(args, configuration):
    client_info = configuration.client_info()
    client = Client(client_info["client_id"], client_info["client_secret"])

    access_token = ""
    try:
        access_token = configuration.access_token()
    except (configparser.NoOptionError, ValueError):
        access_token, exp = client.get_access_token()
        exp = int(time.time()) + exp
        configuration.access_token(access_token, exp)
        
    client.set_access_token(access_token)
    
    user_id = client.get_user_id(configuration.username())
    follows = client.get_follows(user_id)
    onlines = client.get_onlines(follows)

    name = ""
    if len(onlines) != 0:
        name = print_onlines(onlines)
    else:
        print("No one is online!")
        return

    subprocess.run([args.program, f"https://twitch.tv/{name}"])


# Print whos online, and select one to watch
def print_onlines(online: list):
    count = 1

    for on in online:
        print(f'{count}: {on["name"]} | {on["title"]} | Viewers: {on["viewers"]}')
        count += 1

    selection = int(input("Watch: "))

    if selection <= len(online) and selection != 0:
        return online[selection - 1]["name"]
    else:
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", help="open stream in program of choice", type=str)
    parser.add_argument("--client-id", type=str)
    parser.add_argument("--client-secret", type=str)
    parser.add_argument("--username", type=str)

    args = parser.parse_args()
    handle_args(args)


if __name__ == "__main__":
    main()
