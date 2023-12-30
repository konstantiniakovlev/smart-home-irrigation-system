from helpers.pico import Pico, Pump
from helpers.api import PicoAPI
from utils import config


def main():
    pico = Pico()
    pump = Pump(name="Water Pump")
    api = PicoAPI(ctrl_ent=pump)

    pico.connect()
    pico.register()

    api.run(host="0.0.0.0", port=config.PICO_PORT)


def test():
    pump = Pump()
    pump.water(3)


if __name__ == "__main__":
    main()
