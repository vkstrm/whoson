import requests

class Client:

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_access_token(self, access_token: str):
        self.access_token = access_token
        self.default_header = {
            "client-id": self.client_id, 
            "Authorization": f"Bearer {self.access_token}"} 

    # Get id of your follows
    def get_follows(self, user_id: str):
        url = f"https://api.twitch.tv/helix/users/follows?from_id={user_id}&first=100"

        response = requests.get(url, headers=self.default_header)
        response.raise_for_status()
        users = response.json()

        following_ids = []
        for user in users["data"]:
            following_ids.append(user["to_id"])

        payload = {'user_id': following_ids}

        return payload

    # Get which follows are online
    def get_onlines(self, payload: dict):
        url = "https://api.twitch.tv/helix/streams?first=100"

        response = requests.get(url, headers=self.default_header, params=payload)
        response.raise_for_status()
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

    def get_access_token(self) -> (str, str):
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials"

        response = requests.post(url)
        response.raise_for_status()

        body = response.json()
        exp = body["expires_in"]
        return (body["access_token"], exp)

    def get_user_id(self, username: str) -> str:
        url = f"https://api.twitch.tv/helix/users?login={username}"

        response = requests.get(url, headers=self.default_header)
        response.raise_for_status()

        return response.json()["data"][0]["id"]