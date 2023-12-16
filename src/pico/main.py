from utils.connection import connect
from helpers.pico import Pump
from helpers.api import PicoAPI

PORT = 80


def main():
    pump = Pump(obj_id=PORT, name="water pump")

    status = connect()
    api = PicoAPI(
        ctrl_ent=pump,
        host="0.0.0.0",
        port=PORT
    )
    api.expose()


def test():
    pump = Pump()
    pump.water(3)


if __name__ == "__main__":
    main()
