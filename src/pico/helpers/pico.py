import machine
import time


class Pump:

    def __init__(self, obj_id=None, name=None):
        self.obj_id = obj_id
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

