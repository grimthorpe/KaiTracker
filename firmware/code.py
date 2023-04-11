# KaiTracker code.py
#
# SPDXVersion: SPDX-2.3
# SPDX-FileCopyrightText: Copyright 2023 Lisa St.John
# SPDX-License-Identifier: GPL-3.0+

import board
import busio
import digitalio
import supervisor
import storage

OnboardLED=digitalio.DigitalInOut(board.LED)
OnboardLED.direction=digitalio.Direction.OUTPUT
EnableSwitch=digitalio.DigitalInOut(board.GP22)
EnableSwitch.direction=digitalio.Direction.INPUT
EnableSwitch.pull=digitalio.Pull.DOWN

UART=busio.UART(board.GP0, board.GP1, baudrate=9600)

def LogLines(lines):
    if EnableSwitch.value:
        try:
            with open("/kaigpsdata.txt", "a") as fp:
                for line in lines:
                    print(line)
                    fp.write(line)
                fp.close()
        finally:
            pass
    else:
        print('*', end='')    
    
gpsline=''
inGPSdata=False

while True:
    gpsbytes=UART.read(512)
    if gpsbytes is not None:
        lines=[]
        OnboardLED.value=True
        for ch in gpsbytes:
            if inGPSdata:
                gpsline+=chr(ch)
                if ch==13:
                    lines.append(gpsline)
                    gpsline=''
                    inGPSdata=False
            else:
                if ch==36:
                    gpsline='$'
                    inGPSdata=True
        LogLines(lines)
        OnboardLED.value=False
    else:
        sleep(0.1)

