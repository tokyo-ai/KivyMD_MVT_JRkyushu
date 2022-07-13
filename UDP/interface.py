from abc import ABC, abstractmethod


class DetectorClient(ABC):

    @abstractmethod
    def _create_socket(self):
        pass

    @abstractmethod
    def _create_udp_session(self):
        pass

    @abstractmethod
    def receive_request(self):
        pass

    @abstractmethod
    def send_request(self):
        pass

    @abstractmethod
    def receive_response(self):
        pass

    @abstractmethod
    def receive_packet_chunks(self):
        pass

    @abstractmethod
    def send_packet_chunks(self):
        pass

    @abstractmethod
    def send_packet(self):
        pass

