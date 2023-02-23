import json
import logging
from pathlib import Path

import requests
import rich


class ParentType:
    __current_json__ = None

    @classmethod
    def overwrite(cls, td: dict, path: Path, force_json=False):
        from bme.config_mng import Config
        cfg = Config.read()
        if not cfg.get("use-daemon", False) or force_json:
            cls.dump_json(path, td)
            return path

        else:
            try:
                port = cfg.get("daemon-port", 9837)
                requests.post(f"http://localhost:{port}/{cls.__name__.lower()}", json=td)
                return path
            except requests.exceptions.ConnectionError:
                rich.print("[red]BME Daemon not running[/red]")
                raise Exception("BME Daemon not running")

    @classmethod
    def dump_json(cls, path, td):
        # Invalidate cache
        cls.__current_json__ = None
        with open(str(path), "w") as f:
            json.dump(td, f, indent=4)

    @classmethod
    def load_all(cls, path, force_json=False) -> dict:
        from bme.config_mng import Config
        cfg = Config.read()
        if not cfg.get("use-daemon", False) or force_json:
            return cls.read_json(path)
        else:
            try:
                port = cfg.get("daemon-port", 9837)
                ret = requests.get(f"http://localhost:{port}/{cls.__name__.lower()}s")
                return ret.json()
            except requests.exceptions.ConnectionError:
                rich.print("[red]BME Daemon not running[/red]")
                raise Exception("BME Daemon not running")

    @classmethod
    def read_json(cls, path):
        if cls.__current_json__ is None:
            with open(str(path), "r") as f:
                creds = json.load(f)
                logging.debug(f"Loaded {creds}")
                cls.__current_json__ = creds
            return creds

        return cls.__current_json__
