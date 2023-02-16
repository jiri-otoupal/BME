import json

from bme.config import default_config_location


class Config:
    @classmethod
    def init(cls):
        if default_config_location.exists():
            return
        cfg = {"auto-execute": True, "notify-update": True}
        with open(default_config_location, "w") as f:
            json.dump(cfg, f, indent=4)

    @classmethod
    def read(cls):
        cls.init()
        with open(default_config_location, "r") as f:
            return json.load(f)
