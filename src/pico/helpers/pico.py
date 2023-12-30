import machine
import network
import time
import ubinascii

from utils import config
from utils import requests


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

        self._await_connection()
        self._check_connection()

        self.status = "connected"
        self.ip_addr, _, _, _ = self.wlan.ifconfig()
        self.mac_addr = ubinascii.hexlify(self.wlan.config("mac"), ":").decode()
        print("Connected inet", self.ip_addr)

    def register(self):
        self._check_connection()
        self.wlan.active(True)

        url = requests.create_url(endpoint="/devices/register/")
        payload = self._create_payload()
        requests.send_request(url=url, json=payload, method="post")

    def _await_connection(self):
        for _ in range(config.TIMEOUT_TIME):
            if self.wlan.isconnected():
                break
            time.sleep(1)

    def _check_connection(self):
        if not self.wlan.isconnected():
            raise Exception("TimeoutError, pico was not able to connect to network.")

    def _create_payload(self):
        payload = {
            "mac_address": self.mac_addr,
            "ip_address": self.ip_addr,
            "device_type": self.device_type,
            "port": config.PICO_PORT,
            "device_description": "Microcontroller with relay",
            "program_description": "Irrigation pump with moisture sensor"
        }
        return payload


class Pump:

    def __init__(self, name=None):
        self.name = name
        self._configure_hardware()
        self._set_initial_state()

    def _configure_hardware(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.relay = machine.Pin(16, machine.Pin.OUT)

    def _set_initial_state(self):
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

