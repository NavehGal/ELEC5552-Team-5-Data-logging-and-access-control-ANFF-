# This script runs on local machine (NOT XBEE).
# Connected XBee should be in API mode.

from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
import time
from digi.xbee.devices import XBee64BitAddress

# This is for USB connection i.e. via Explorer Dongle
device = XBeeDevice("COM3", 19200)
device.open()

hub = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20042284B97"))
device.send_data(hub, "Hello XBee!")


# Send data using the remote object.

# Callback function runs any time the respective event is triggered.
def data_received_callback(transmission):
    data = transmission.data
    device.flush_queues()
    data = bytearray.decode(data, 'utf-8')
    print("Message: %s" % data)


device.add_data_received_callback(data_received_callback)

print("Waiting...")

while True:
    time.sleep(0.01)
