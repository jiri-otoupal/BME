from datetime import datetime

import lastversion
import requests
import rich
import semantic_version
from requests import ConnectTimeout, ReadTimeout

from bme import __version__
from bme.config_mng import Config


class Notifier:
    @classmethod
    def check_pypi_available(cls):
        try:
            # TODO: Connection timeout fix
            req = requests.get("https://pypi.org/", timeout=0.2)
            return req.status_code == 200
        except (ConnectTimeout, ReadTimeout):
            return False

    @classmethod
    def get_last_version(cls):
        return lastversion.latest(__version__.__pypi_repo__)

    @classmethod
    def is_last_version(cls):
        last = cls.get_last_version()
        return semantic_version.Version(
            __version__.__version__) >= semantic_version.Version(str(last))

    @classmethod
    def notify(cls):
        config = Config.read()
        dt = datetime.now()

        if (dt - datetime.fromtimestamp(
                config.get("last-check", 1677884000))).seconds < 60 * 60 * 8:
            return

        config["last-check"] = datetime.timestamp(dt)

        if cls.check_pypi_available() and not cls.is_last_version():
            last = cls.get_last_version()
            rich.print(
                f"[yellow]WARNING: You are using bme version {__version__.__version__}; however,"
                f" version {last} is available.[/yellow]")
            rich.print(
                f"[yellow]You should consider upgrading via the `[green]pip3 install bme --upgrade[/green]`"
                f" command.[/yellow]")
