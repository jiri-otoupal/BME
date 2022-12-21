import os
import subprocess
from pathlib import Path


class History:
    @classmethod
    def add_cmd(cls, cmd):
        r = os.system(f"history -a {cmd}")
        return r == 32512
