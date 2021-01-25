from pathlib import Path
import time
import configparser

WHOSON_SECTION = "WHOSON"

class Configuration:

    def __init__(self):
        self.config_filename = ".whoson.ini"
        self.config_path = Path.home().joinpath(self.config_filename)

        self.config = configparser.ConfigParser()
        if not self.config_path.exists():
            print(f"No config file, creating one at {self.config_path.absolute()}")

            self.config.add_section(WHOSON_SECTION)
            with self.config_path.open('w') as f:
                self.config.write(f)
        
        with self.config_path.open('r') as f:
            self.config.read_file(f)

    def client_info(self, client_info: dict = None) -> dict:
        return {
            "client_id": self.config.get(WHOSON_SECTION,"client_id"),
            "client_secret": self.config.get(WHOSON_SECTION,"client_secret")}

    def client_id(self, client_id: str):
        self.config.set(WHOSON_SECTION,"client_id", client_id)
        self.save_config()

    def client_secret(self, client_secret: str):
        self.config.set(WHOSON_SECTION,"client_secret", client_secret)
        self.save_config()

    def username(self, username: str = None) -> str:
        if username is None:
            return self.config.get(WHOSON_SECTION,"username")

        self.config.set(WHOSON_SECTION,"username", username)
        self.save_config()
        
    def access_token(self, access_token: str = None, exp: int = None) -> str:
        if access_token is None:
            exp = int(self.config.get(WHOSON_SECTION,"exp"))
            if time.time() > exp:
                raise ValueError

            return self.config.get(WHOSON_SECTION,"access_token")

        self.config.set(WHOSON_SECTION,"exp", str(exp))
        self.config.set(WHOSON_SECTION,"access_token", access_token)
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as f:
                self.config.write(f)
        