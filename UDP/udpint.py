from abc import ABC, abstractmethod


class UDPInterface(ABC):
    @abstractmethod
    def send_request(self): pass

    @abstractmethod
    def send_response(self): pass

    @abstractmethod
    def receive_response(self): pass


    @abstractmethod
    def create_data_socket(self): pass   #create data and command sockets

    @abstractmethod
    def create_data_buffer_chunks(self): pass

    @abstractmethod
    def send_data_buffer_chunks(self): pass

    @abstractmethod
    def receive_data_buffer_chunks(self): pass

    @abstractmethod
    def create_data_buffer_mono(self): pass

    @abstractmethod
    def receive_data_buffer_mono(self): pass
