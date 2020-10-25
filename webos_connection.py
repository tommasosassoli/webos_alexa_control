from wakeonlan import send_magic_packet
from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl, MediaControl
import json


class WebOsConnection:

    def __init__(self):#TODO pass args
        with open('tv_conf.json', 'r') as fileConf:#TODO do not read from file
            dataConf = fileConf.read()
        self.store = json.loads(dataConf)

        self.clientIp = self.store['ip_address']
        self.macAddress = self.store['mac_address']
        self.tvName = self.store['name']
        self.client = WebOSClient(self.clientIp)
        self.isConnected = False
        self.systemControl = None
        self.mediaControl = None

    def get_client(self):
        if self.isConnected is False:
            # Wake on lan
            send_magic_packet(self.macAddress)

            #connect to the host
            self.client.connect()
            for status in self.client.register(self.store):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    print("Registration successful!")
                    self.isConnected = True
        return self.client

    def disconnect_client(self):
        self.isConnected = False

    def switchOn(self):
        if self.systemControl is None:
            self.systemControl = SystemControl(self.get_client())
        #self.systemControl.power_on()
        #TODO non esiste power_on()

    def switchOff(self):
        if self.systemControl is None:
            self.systemControl = SystemControl(self.get_client())
        self.systemControl.power_off()
        self.disconnect_client()

    def setVolume(self, volume):
        if self.mediaControl is None:
            self.mediaControl = MediaControl(self.get_client())
        self.mediaControl.set_volume(volume)
