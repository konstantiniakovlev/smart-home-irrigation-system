import machine
import network
import time
import ubinascii
import urequests as requests
from utils import config


class Pico:

    def __init__(self):
        self.wlan = None
        self.ip_addr = None
        self.mac_addr = None
        self.device_type = "Raspberry Pi Pico W"
        self.status = "disconnected"

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PWD)

        for _ in range(config.TIMEOUT_TIME):
            if self.wlan.isconnected():
                break
            time.sleep(1)

        if not self.wlan.isconnected():
            raise Exception(
                "TimeoutError, pico was not able to connect to network."
            )

        self.status = "connected"
        self.ip_addr, _, _, _ = self.wlan.ifconfig()
        print("Connected inet", self.ip_addr)

    def register(self):
        if not self.wlan.isconnected():
            print("Device is not connected to network. Connect before registering device.")

        self.wlan.active(True)
        self.mac_addr = ubinascii.hexlify(
            self.wlan.config("mac"),
            ":"
        ).decode()

        base_url = f"http://{config.CONTROLLER_HOST}:{config.CONTROLLER_PORT}"
        url = base_url + "/devices/register/"
        payload = {
            "mac_address": self.mac_addr,
            "ip_address": self.ip_addr,
            "device_type": self.device_type,
            "port": config.PICO_PORT,
            "device_description": "Microcontroller with relay",
            "program_description": "Irrigation pump with moisture sensor"
        }
        response = requests.post(url=url, json=payload)
        if response.status_code not in [200, 201]:
            raise Exception(f"{response.status_code}, {response.content}")


class Pump:

    def __init__(self, name=None):
        self.name = name
        self._configure_hardware()

    def _configure_hardware(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.relay = machine.Pin(16, machine.Pin.OUT)

        self.led.off()
        self.relay.value(1)

    def water(self, water_time):

        self.led.on()
        self.relay.value(0)

        time.sleep(water_time)

        self.relay.value(1)
        self.led.off()


class MoistureSensor:

    def __init__(self):
        pass

    def get_soil_humidity(self):
        pass

