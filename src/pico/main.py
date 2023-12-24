from helpers.pico import Pico, Pump
from helpers.api import PicoAPI
from utils import config


def main():

    pico = Pico()
    pico.connect()
    pico.register()

    pump = Pump(name="Water Pump")

    api = PicoAPI(
        ctrl_ent=pump,
        host="0.0.0.0",
        port=config.PICO_PORT
    )  # todo: parse request, create response
    api.run()


def test():
    pump = Pump()
    pump.water(3)


if __name__ == "__main__":
    main()
