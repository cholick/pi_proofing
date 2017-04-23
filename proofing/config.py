import json


class Config():
    def __init__(self, file='config.json'):
        with open(file) as config_file:
            config = json.load(config_file)

        self.serial = config["serial"]
        self.switch_pin = config["switchPin"]
        self.temp = config["temp"]
