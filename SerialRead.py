import time as tim
import serial
import struct
import threading
port = "COM15"
dollar = b'$GPRMC'
x = ' '
can = b'403'
time = ""
longitude = ""
latitude = ""
speed = 0
gpsSpeed = ""
date = ""
batteryCell = [0] * 30
splitVar = b" "
volts = 0
amps = 0
rpm = 1000
energy = 0
odometer = 0
commandAcAmps = 0
commandRpm = 0
commandDcAmps = 0
trackers = [0] * 6
packCurrent = 0
packVoltage = 0
packSoc = 0
packRelay = 0
chargeILimit = 0
packAH = 0
highModTemp = 0
lowModTemp = 0
highModV = 0
lowModV = 0
highVModID = 0
lowVModID = 0

# file = open("log.txt", "wb")

ser = serial.Serial(
    port=port,
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

counter = 0


def rd(inBytes):
    inList = inBytes.rstrip(b'\r\n').split(b',.')  # split byte in message from serial
    for i in range(len(inList)):
        if inList[i] == b'':
            inList[i] = b'/x00'
    return (b''.join(inList))


def serRead():
    global time, longitude, latitude, gpsSpeed, batteryCell, volts, amps, speed, rpm, energy, odometer
    global commandAcAmps, commandRpm, commandDcAmps, trackers, packCurrent, packVoltage, packSoc, packRelay
    global chargeILimit, packAH, highModTemp, lowModTemp, highModV, lowModV, highVModID, lowVModID
    while 1:
        rpm = rpm + 1
        x = ser.readline()
        try:
            if (len(x) == 0):  # if the string is empty
                pass
            elif (x.startswith(dollar)):
                y = x.split(",")
                time = y[1]
                longitude = y[5]
                latitude = y[3]
                gpsSpeed = y[7]
                date = y[9]
            elif (x.startswith(b'36')):
                y = x.split(splitVar)
                z = struct.unpack("Bxxxf", rd(y[1]))
                batteryCell[z[0]] = z[1]
            elif (x.startswith(b'402')):
                y = x.split(splitVar)
                z = struct.unpack("ff", rd(y[1]))
                volts = z[0]
                amps = z[1]
            elif (x.startswith(b'403')):
                y = x.split(splitVar)
                z = struct.unpack("ff", rd(y[1]))
                speed = z[0]
                rpm = z[1]
            elif (x.startswith(b'40e')):
                y = x.split(splitVar)
                z = struct.unpack("ff", rd(y[1]))
                energy = z[0]
                odometer = z[1]
            elif (x.startswith(b'501')):
                y = x.split(splitVar)
                z = struct.unpack("ff", rd(y[1]))
                commandAcAmps = z[0]
                commandRpm = z[1]
            elif (x.startswith(b'502')):
                y = x.split(splitVar)
                z = struct.unpack("ff".rd(y[1]))
                commandDcAmps = z[0]
            elif (x.startswith(b'60')):
                y = x.split(splitVar)
                z = struct.unpack("<hhhh", rd(y[1]))
                trackers[int(y[0]) - 600] = z
            elif (x.startswith(b'6B0')):
                y = x.split(splitVar)
                z = struct.unpack("<BxxBhh", rd(y[1]))
                #                 print(z)
                packCurrent = z[0]
                packVoltage = z[1]
                packSoc = z[2]
                packRelay = z[3]
            elif (x.startswith(b'6B1')):
                y = x.split(splitVar)
                z = struct.unpack(">hhBBBB", rd(y[1]))
                chargeILimit = z[0]
                packAH = z[1]
                highModTemp = z[2]
                lowModTemp = z[3]
            elif (x.startswith(b'6B2')):
                y = x.split(splitVar)
                z = struct.unpack(">HHBBBB", rd(y[1]))
                highModV = z[0]
                lowModV = z[1]
            elif (x.startswith(b'6B3')):
                y = x.split(splitVar)
                z = struct.unpack("BBxxxxxx", rd(y[1]))
                highVModID = z[0]
                lowVModID = z[1]
        except:
            print('error')
            pass


t1 = threading.Thread(target=serRead)
t1.start()
