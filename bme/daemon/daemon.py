import uvicorn as uvicorn

from bme.config_mng import Config


class Daemon:

    @classmethod
    def start(cls):
        from bme.daemon.api import app
        cfg = Config.read()
        port = cfg.get("daemon-port", 9837)
        uvicorn.run(app, host="localhost", port=port)


if __name__ == "__main__":
    Daemon.start()
