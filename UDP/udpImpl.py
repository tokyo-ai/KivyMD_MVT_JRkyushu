import os
import pickle
import socket
import time
import cv2
import numpy

from UDP.udpint import UDPInterface


class UDPImplt(UDPInterface):
    data_buffer_size = 576 * 1024
    timeout_trial = 10
    scale_percent = 80

    def __init__(
            self,
            local_host: str,
            local_port: int,
            receive_host: str,
            receive_port: int,
            udp_packet_number: int,
            timeout_trial: float,
    ):
        self._local_host = local_host
        self._local_port = local_port
        self._receive_host = receive_host
        self._receive_port = receive_port
        self._udp_packet_number = udp_packet_number
        self._timeout_trial = timeout_trial

        # Create socket to receive data
        self._data_socket = self._create_data_socket(
            host=self._local_host, port=self._local_port, timeout=self._timeout_trial
        )

    @property
    def datasocket(self):
        return self._data_socket

    @property
    def update_data_socket(self):
        self._data_socket = self._create_data_socket(
            host=self._local_host, port=self._local_port, timeout=self._timeout_trial
        )
        return self._data_socket

    @staticmethod
    def _create_data_socket(host: str, port: int, timeout: float):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            data_socket.bind((host, port))
        except OSError:
            data_socket.shutdown(socket.SHUT_RD)
            data_socket.close()
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            pass
        data_socket.settimeout(timeout)
        return data_socket

    @staticmethod
    def send_request(sock: socket, listen_host: str, listen_port: int, data_bytes):
        sock.sendto(data_bytes, (listen_host, listen_port))

    @staticmethod
    def send_data_buffer_chunks(
            sock: socket, listen_host: str, listen_port: int, data_bytes_list
    ):
        for data_byte in data_bytes_list:
            sock.sendto(data_byte, (listen_host, listen_port))
            time.sleep(0.01)

    @staticmethod
    def receive_data_buffer_mono(self, sock: socket):
        try:
            buf, receive_from_addr = sock.recvfrom(self.data_buffer_size)
            data_dict = pickle.loads(buf)
            preview_jpg: bytes = data_dict["preview"]
            preview_filename: bytes = data_dict["filename"]
            return preview_jpg, preview_filename
        except socket.timeout:
            sock = self._restart_socket(sock, self._local_host, self._local_port)
        except OSError as err:
            sock = self._restart_socket(sock, self._local_host, self._local_port)
            return None

    @staticmethod
    def receive_data_buffer_chunks(self, sock: socket):
        try:
            index = 0
            while index < self._udp_packet_number - 1:
                buf, receive_from_addr = sock.recvfrom(self.data_buffer_size)
                data_dict = pickle.loads(buf)
                preview_index: bytes = data_dict["index"]
                preview_filename: bytes = data_dict["filename"]
                index = int.from_bytes(preview_index, byteorder="big")

                if index == 0:
                    preview_bytes: bytes = data_dict["preview"]
                else:
                    preview_bytes += data_dict["preview"]

            return preview_bytes, preview_filename
        except socket.timeout:
            sock = self._restart_socket(sock, self._local_host, self._local_port)
        except OSError as err:
            sock = self._restart_socket(sock, self._local_host, self._local_port)
            return None

    @staticmethod
    def receive_response(self, sock: socket):
        try:
            buf, receive_from_addr = sock.recvfrom(self.data_buffer_size)
            return buf
        except OSError as err:
            sock = self._restart_socket(sock, self._local_host, self._local_port)
        except socket.timeout:
            sock = self._restart_socket(
                sock, self._local_host, self._local_port
            )  # if timeout, recreate the socket
            return None

    def _restart_socket(self, sock: socket, host: str, port: int):
        sock.shutdown(socket.SHUT_RD)
        sock.close()
        return self._create_data_socket(host, port, self.timeout_trial)

    def create_data_buffer_mono(self, preview_filename, ext=".jpg"):
        preview_nparray = self.openCV_file(preview_filename)
        preview_filename = self._resize_img(
            scale_percent=15, img_nparray=preview_nparray
        )
        ret, encoded_preview = cv2.imencode(ext=ext, img=preview_filename)
        buffer = pickle.dumps(dict(preview=encoded_preview.tobytes()), protocol=3)
        return buffer if buffer.__len__() < self.data_buffer_size else None

    def create_data_buffer_chunks(self, preview_filename: str, ext=".png"):
        preview_nparray = self.openCV_file(preview_filename)
        ret, encoded_preview = cv2.imencode(ext=ext, img=preview_nparray)
        buffer_list = numpy.array_split(encoded_preview, self._udp_packet_number)
        res = []
        for i in range(self._udp_packet_number):
            buffer = pickle.dumps(
                dict(
                    index=i.to_bytes(2, byteorder="big"),
                    preview=buffer_list[i].tobytes(),
                    filename=preview_filename.encode("utf-8"),
                ),
                protocol=3,
            )
            res.append(buffer)
        return res

    def _resize_img(self, scale_percent: float, img_nparray: numpy.ndarray):
        width = int(img_nparray.shape[1] * scale_percent / 100)
        height = int(img_nparray.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img_nparray, dim, interpolation=cv2.INTER_AREA)
        return resized

    def openCV_file(self, filename) -> numpy.ndarray:
        basedir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(basedir, filename)
        filebytes = cv2.imread(target_path, cv2.IMREAD_UNCHANGED)
        return filebytes
