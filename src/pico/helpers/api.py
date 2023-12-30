import json
import socket
import time
from utils import config


class PicoAPI:

    def __init__(self, ctrl_ent):
        self.pump = ctrl_ent
        self.socket_obj = None
        self.connection = None

    def run(self, host="0.0.0.0", port=80):
        address_info = socket.getaddrinfo(host, port)
        self._create_socket(address_info)

        while True:
            self._accept_connection()
            data = self._receive_request()
            method, endpoint, params, headers = self._parse_request(data)
            print(method, endpoint, params, headers)
            response = self._create_response(params)
            self._send_response(response)
            self._complete_request(endpoint, params)

    def _create_socket(self, address_info):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(address_info[0][-1])
        self.socket_obj.listen(2)
        print("listening on address", address_info[0][-1])

    def _accept_connection(self):
        try:
            self.connection, address = self.socket_obj.accept()
            print(self._custom_strftime(time.localtime()))
            print("Client connected from", address)
        except OSError as e:
            raise Exception(e)

    def _receive_request(self):
        try:
            request = self.connection.recv(1024)
            data = request.decode("utf-8")
            return data
        except OSError as e:
            raise Exception(e)

    def _parse_request(self, data):
        try:
            request_line, headers = data.split("\r\n", 1)
            method = self._parse_method(request_line)
            endpoint = self._parse_endpoint(request_line)
            params = self._parse_params(request_line)
            return method, endpoint, params, headers
        except OSError as e:
            raise Exception(e)

    def _create_response(self, params):
        response = dict({
            "name": self.pump.name,
            "time_active": 0,
            "start_time": None
        })
        response["time_active"] = int(params.get("duration", config.IDEAL_DURATION))
        response["start_time"] = self._custom_strftime(time.localtime())
        return json.dumps(response)

    def _send_response(self, response):
        try:
            self.connection.sendall("HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n")
            self.connection.sendall(bytes(response, "utf-8"))
            self.connection.close()
        except OSError as e:
            raise Exception(e)

    def _complete_request(self, endpoint, params):
        if "/relay/on" in endpoint:
            self.pump.water(int(params.get("duration", config.IDEAL_DURATION)))

    @staticmethod
    def _parse_method(request_line):
        if "GET" in request_line:
            return request_line.split()[0]
        else:
            raise Exception("Method does not exist")

    @staticmethod
    def _parse_endpoint(request_line):
        url = request_line.split()[1]
        return url.split("?")[0]

    @staticmethod
    def _parse_params(request_line):
        url = request_line.split()[1]
        if "?" not in url:
            return dict()
        else:
            params = dict()
            params_list = url.split("?")[1].split("&")
            for kv in params_list:
                key, value = kv.split("=")
                params[key] = value
            return params

    @staticmethod
    def _custom_strftime(dt):
        year, month, day = dt[0:3]
        hour, minute, second = dt[3:6]
        dt_str = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            year, month, day, hour, minute, second
        )
        return dt_str
