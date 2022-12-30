import datetime
import os
import time

import rich

from bme.config import default_sequences_location
from bme.saved_types.bookmark import Bookmark
from bme.saved_types.parent_type import ParentType


class Sequence(ParentType):
    @classmethod
    def init(cls):
        default_sequences_location.parent.mkdir(exist_ok=True)
        if not default_sequences_location.exists():
            cls.overwrite({}, default_sequences_location)

    @classmethod
    def create(cls, name: str):
        sequences = cls.load_all(default_sequences_location)
        if name in sequences.keys():
            return False
        sequences[name] = {"created-time": str(datetime.datetime.utcnow()),
                           "cmds": []}
        cls.overwrite(sequences, default_sequences_location)
        return True

    @classmethod
    def remove(cls, name: str):
        sequences = cls.load_all(default_sequences_location)
        if name not in sequences.keys():
            return False
        sequences.pop(name)
        cls.overwrite(sequences, default_sequences_location)
        return True

    @classmethod
    def pop_cmd(cls, name: str):
        sequences = cls.load_all(default_sequences_location)
        try:
            sequences.pop(name)
            cls.overwrite(sequences, default_sequences_location)
            return True
        except ValueError:
            return False

    @classmethod
    def execute(cls, name, verbose: bool = False):
        """
        Execute sequence in current workdir
        @param verbose: Be verbose about what is happening in sequence
        @param name:
        @return:
        """
        rich.print(f"Executing Sequence '{name}'")
        sequences = cls.load_all(default_sequences_location)
        if name not in sequences.keys():
            return False

        sequence = sequences[name]
        cmds = sequence["cmds"]
        for cmd in cmds:
            if verbose:
                rich.print(f"Executing... {cmd}")
            os.system(cmd)
        return True

    @classmethod
    def add_cmd(cls, seq_name: str, cmd: str):
        return Bookmark.append(cmd, location=default_sequences_location,
                               root_key=seq_name)

    @classmethod
    def rm_cmd(cls, seq_name: str, cmd):
        return Bookmark.remove(cmd, location=default_sequences_location,
                               root_key=seq_name)
