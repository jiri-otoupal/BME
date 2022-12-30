from pathlib import Path
from typing import Optional

from escapejson import escapejson

from bme.config import default_bookmarks_location
from bme.saved_types.parent_type import ParentType


class Bookmark(ParentType):
    @classmethod
    def init(cls):
        default_bookmarks_location.parent.mkdir(exist_ok=True)
        if not default_bookmarks_location.exists():
            cls.overwrite({"cmds": []}, default_bookmarks_location)

    @classmethod
    def remove(cls, cmd: str, location=default_bookmarks_location,
               root_key: Optional[str] = None):
        history = cls.load_history(location, root_key)
        if cmd in history["cmds"]:
            history["cmds"].remove(escapejson(cmd))

            if root_key:
                full_history = cls.load_all(location)
                full_history[root_key] = history
                history = full_history

            cls.overwrite(history, location)
            return True
        else:
            return False

    @classmethod
    def append(cls, cmd: str, location=default_bookmarks_location,
               root_key: Optional[str] = None):
        if root_key:
            history = cls.load_all(location)[root_key]
        else:
            history = cls.load_all(location)
        if cmd in history["cmds"]:
            return False
        history["cmds"].append(escapejson(cmd))

        if root_key:
            full_history = cls.load_all(location)
            full_history[root_key] = history
            history = full_history

        cls.overwrite(history, location)
        return True

    @classmethod
    def load_history(cls, location: Path, root_key: str):
        if root_key:
            history = cls.load_all(location)[root_key]
        else:
            history = cls.load_all(location)
        return history
