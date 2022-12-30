import json
import logging
from pathlib import Path


class ParentType:
    @classmethod
    def overwrite(cls, td: dict, path: Path):
        with open(str(path), "w") as f:
            json.dump(td, f, indent=4)
        return path

    @classmethod
    def load_all(cls, path) -> dict:
        with open(str(path), "r") as f:
            creds = json.load(f)
            logging.debug(f"Loaded {creds}")
        return creds
