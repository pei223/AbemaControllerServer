import json


class Config:
    _KEY_IP_ADDRESS = "ip_address"
    _KEY_PORT = "port"
    _KEY_ABEMA_URL = "abema_url"
    _KEY_DEFAULT_CHANNEL = "default_channel"
    _KEY_DRIVER_PATH = "driver_path"

    _config = None

    def __init__(self):
        with open("./config.json", "r") as file:
            json_obj = json.load(file)
            self.ip_address = json_obj[self._KEY_IP_ADDRESS]
            self.port = json_obj[self._KEY_PORT]
            self.abema_url = json_obj[self._KEY_ABEMA_URL]
            self.default_channel = json_obj[self._KEY_DEFAULT_CHANNEL]
            self.driver_path = json_obj[self._KEY_DRIVER_PATH]

    def abema_channel_url(self):
        return "{}/{}".format(self.abema_url, self.default_channel)

    @classmethod
    def instance(cls):
        if not cls._config:
            cls._config = Config()
        return cls._config
