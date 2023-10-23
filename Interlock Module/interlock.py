import tinytuya
import time

def read_output_file(filepath):
    with open(filepath, 'r') as f:
        value = f.read().strip()
    return value

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='bf2d4af68dd642eeac8qpn',
    address='172.20.10.8',
    local_key='rB5(EM%}Qc$Vq?fX', 
    version=3.4)

file_path = "/home/pi/isolatorOutput.txt"
previous_value = None  # to store the last known value

while True:
    current_value = read_output_file(file_path)

    # Only act if the value has changed
    if current_value != previous_value:
        if current_value == "1":
            d.turn_on()
        elif current_value == "0":
            d.turn_off()
        else:
            print(f"Unexpected value '{current_value}' in {file_path}. Expected '1' or '0'.")
        previous_value = current_value  # update the last known value

    time.sleep(1)  # wait for 1 second before checking again
