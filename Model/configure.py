from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class ConfigureModel(Widget):
    _server_ip_address = StringProperty(None)
    _server_port_num = StringProperty(None)

    def __init__(self):
        self._server_ip_address = '192.168.1.1'
        self._server_port_num = '60001'
        self._observers = []

    @property
    def server_info(self):
        return (self._server_ip_address, self._server_port_num)

    def set_server_ip_address(self, value: str):
        self._server_ip_address = value
        self.notify_observers()

    def set_server_port(self, value: str):
        self._server_port_num = value
        self.notify_observers()

    def set_server_info(self, value: (str, str)):
        self._server_ip_address, self._server_port_num = value
        self.notify_observers()

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()
