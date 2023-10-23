import board
import busio
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()
print("Waiting for RFID/NFC card...")

while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is not None:
        uid_str = ''.join([hex(i)[2:].zfill(2) for i in uid])
        print("Found card with UID:", uid_str)

        # Read the UID.txt file
        with open('/home/pi/credentialList/UID.txt', 'r') as uid_file:
            uid_list = [line.strip() for line in uid_file]

        # If the UID is in the uid_list, toggle the content of isolatorOutput.txt
        if uid_str in uid_list:
            with open('/home/pi/isolatorOutput.txt', 'r') as output_file:
                current_value = output_file.readline().strip()

            if current_value == "1":
                new_value = "0"
            else:
                new_value = "1"
            
            with open('/home/pi/isolatorOutput.txt', 'w') as output_file:
                output_file.write(new_value + "\n")
            
            print(f"Value toggled to {new_value} in isolatorOutput.txt")
        else:
            print("UID not in the list. No changes made to isolatorOutput.txt")

        # Wait until the card is removed
        while pn532.read_passive_target(timeout=0.5) is not None:
            pass

        print("Card removed. Waiting for a new card...")
