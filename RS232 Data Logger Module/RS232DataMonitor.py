import time
import xbee
import sys

# Hard-coding in the address of the Hub XBee
brain_id = b'\x00\x13\xA2\x00\x42\x28\x4B\x97'
data = 0
process = False

bytelist = bytes(range(1, 11))
stringbyt = bytelist.decode('utf-8')

commandA = "!%A1?(46)(149)"
commandW = "!#W(143)(53)"
time.sleep_ms(10000)
while True:
    time.sleep_ms(850)  # Polling rate: 1Hz
    # Estimate to include dataread time and computation

    # Need to process W response to determine if process is running
    sys.stdout.write(commandW)
    time.sleep_ms(90)  # Wait for ~200bytes of data
    respW = sys.stdin.read().decode('utf-8')
    Wtemp = respW.split("_")
    Wtext = list(filter(None, Wtemp))
    # Remove the first and last elements, they are junk data
    Wtext.pop(0)
    Wtext.pop()

    # If non-zero rate, proceed, otherwise go back to waiting
    if int(Wtext[0]) > 0.00:
        if not process:
            process = True
        Wtext = ' '.join(Wtext)
        sys.stdout.write(commandA)
        time.sleep_ms(25)
        # Extract tooling, zratio, density from "A" response
        respA = sys.stdin.read().decode('utf-8')
        Atext = respA.split("_")
        Atext = list(filter(None, Atext))
        Atext = Atext[1:4]
        # Send data together as the hub expects it to arrive
        message = "B " + ' '.join(Atext) + Wtext
        try:
            xbee.transmit(brain_id, message)
            print("Transmit Success")
        except Exception as e:
            print("Transmit Failed: %s" % str(e))

    else:
        # This if is triggered if the module expects valid data but receives a zero rate,
        # meaning the process has just finished.
        if process:
            process = False
            try:
                xbee.transmit(brain_id, "B end")
                print("Transmit Success")
            except Exception as e:
                print("Transmit Failed: %s" % str(e))
