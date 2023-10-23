import pytuya

def control_tuya_switch():
    DEVICE_ID = 'bf2d4af68dd642eeac8qpn'
    IP_ADDRESS = '192.168.10.112'
    LOCAL_KEY = '<:s@_alTE]BE~<X+'

    d = pytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
    d.set_version(3.3)
    data = d.status()  
    print("Full data returned from device:", data)
    
    if 'dps' in data and '1' in data['dps']:
        print('Device %s at %s is power state: %s' % 
              (DEVICE_ID, IP_ADDRESS, data['dps']['1']))

        
        d.turn_on()

    else:
        print("Unable to retrieve power state from device.")
