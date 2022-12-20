import json
import logging
from pathlib import Path

from bme.config import default_bookmarks_location


class Bookmark:
    @classmethod
    def init(cls):
        default_bookmarks_location.parent.mkdir(exist_ok=True)
        if not default_bookmarks_location.exists():
            cls.overwrite({"cmds": []}, default_bookmarks_location)

    @classmethod
    def remove(cls, cmd: str):
        history = cls.load_all()
        try:
            history["cmds"].remove(cmd)
            cls.overwrite(history, default_bookmarks_location)
            return True
        except ValueError:
            return False

    @classmethod
    def append(cls, cmd: str):
        history = cls.load_all()
        if cmd in history["cmds"]:
            return False
        history["cmds"].append(cmd)
        cls.overwrite(history, default_bookmarks_location)
        return True

    @classmethod
    def overwrite(cls, td: dict, path: Path):
        with open(str(path), "w") as f:
            json.dump(td, f, indent=4)
        return path

    @classmethod
    def load_all(cls, path=default_bookmarks_location) -> dict:
        with open(str(path), "r") as f:
            creds = json.load(f)
            logging.debug(f"Loaded History {creds}")
        return creds
