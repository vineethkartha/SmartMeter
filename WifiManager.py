import network
import time

from machine import Pin

class WifiManager:
    """ This class is used to establish a connection to the wifi network."""
    
    def __init__(self, ip_config_tuple, connection_retries=10):
        """ The constructor accepts a tuple containing the ip, subnet, gateway, dns also a value on how many times connection retry should be attempted."""
        
        self.wlan = network.WLAN(network.STA_IF)
        self.connection_retries = connection_retries
        self.wlan.ifconfig(ip_config_tuple)
        
    def connect_to_network(self, ssid, password):
        self.wlan.active(True)
        self.wlan.config(pm = network.WLAN.PM_NONE)  # Disable power-save mode
        self.wlan.connect(ssid, password)
        
        attempt = 0
        while attempt < self.connection_retries:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            attempt += 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])
            
        
