#!/usr/bin/env python3

#
#   See who is live on twitch and watch stream in VLC.
#   Assumes you have a twitch api client id, and streamlink installed.
#   Doesn't work well if you follow more than 100 people
#

import requests
import subprocess
import creds // Your info in a separate file

headers = {'Client-ID': '{}'.format(creds.clientid)}

# Get id of your follows
def get_follows():
    followerQuery = "https://api.twitch.tv/helix/users/follows?from_id={}&first=100".format(creds.user_id)

    response = requests.get(followerQuery, headers=headers)
    users = response.json()

    following_ids = []
    for user in users["data"]:
        following_ids.append(user["to_id"])

    payload = {'user_id': following_ids}

    return payload

# Get which follows are online
def get_onlines(payload):
    streamsQuery = "https://api.twitch.tv/helix/streams?first=100"

    response = requests.get(streamsQuery, headers=headers, params=payload)
    streams = response.json()

    online = []
    for stream in streams["data"]:
        online.append({
            'name': stream["user_name"],
            'gameid': stream["game_id"],
            'title': stream["title"],
            'viewers': stream["viewer_count"],
        })

    return online


# Print whos online, and select one to watch
def print_onlines(online):
    count = 1

    for on in online:
        print(f'{count}: {on["name"]} | {on["title"]} | Viewers: {on["viewers"]}')
        count += 1

    selection = int(input("Watch: "))

    if selection <= len(online) and selection != 0:
        return online[selection - 1]["name"]
    else:
        return 0


# Start selected stream
def start_stream(name):
        subprocess.run(["streamlink", "twitch.tv/{}".format(name), "best"])


def main():
    follows = get_follows()
    onlines = get_onlines(follows)
    if len(onlines) != 0:
        name = print_onlines(onlines)
        if name:
            start_stream(name)
    else:
        print("No one is online!")

if __name__ == "__main__":
    main()
    
