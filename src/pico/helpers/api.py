import json
import socket
import time


class PicoAPI:

    def __init__(self, ctrl_ent, host="0.0.0.0", port=80):
        self.pump = ctrl_ent
        self.host = host
        self.port = port
        self.address_info = socket.getaddrinfo(self.host, self.port)
        self.socket_obj = None

    def _create_socket(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(self.address_info[0][-1])
        self.socket_obj.listen(2)
        print("listening on address", self.address_info[0][-1])

    def _get_response(self, request_url, headers):
        response = {
            "object_id": self.pump.obj_id,
            "name": self.pump.name,
            "status": "not active",
            "time_active": 0
        }

        if "/relay/on" in request_url:
            self.pump.water(3)
            response["status"] = "active"
            response["time_active"] = 3

        return json.dumps(response)

    def expose(self):
        self._create_socket()

        while True:
            try:
                connection, address = self.socket_obj.accept()
                print("client connected from", address)

                request = connection.recv(1024)
                data = request.decode("utf-8")
                request_line, headers = data.split("\r\n", 1)

                print(time.localtime())
                print(data)

                response = self._get_response(request_line, headers)

                connection.sendall("HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n")
                connection.sendall(bytes(response, "utf-8"))
                connection.close()

            except OSError as e:
                print(e)
                raise ConnectionError("connection was closed or lost")



