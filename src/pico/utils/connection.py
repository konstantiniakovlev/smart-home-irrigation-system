import network
import utils.config as config
import time

TIMEOUT_TIME = 30


def connect():

    print("waiting for network connection")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(config.WIFI_SSID, config.WIFI_PWD)

    for _ in range(TIMEOUT_TIME):
        if sta_if.isconnected():
            break
        time.sleep(1)

    if not sta_if.isconnected():
        raise TimeoutError("connection timeout, took too long to respond")

    status = sta_if.ifconfig()
    print(f"connected\nIP:", status[0])

    return status
