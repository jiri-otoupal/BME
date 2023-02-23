import json

from bme.config import default_config_location


class Config:
    default_cfg = {"auto-execute": True, "notify-update": True, "use-daemon": False,
                   "daemon-port": 9837, "hostname": "localhost"}

    @classmethod
    def init(cls):
        if default_config_location.exists():
            return

        cls.write_config(cls.default_cfg)

    @classmethod
    def write_config(cls, cfg):
        with open(default_config_location, "w") as f:
            json.dump(cfg, f, indent=4)

    @classmethod
    def fix_integrity(cls):
        read = cls.read()
        cc = set(read.keys())
        dc = set(cls.default_cfg.keys())
        missing_keys = dc - cc

        for key in missing_keys:
            read[key] = cls.default_cfg[key]

        cls.write_config(read)

    @classmethod
    def read(cls) -> dict:
        cls.init()
        with open(default_config_location, "r") as f:
            return json.load(f)
