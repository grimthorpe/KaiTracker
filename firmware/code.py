# KaiTracker code.py
#
# SPDXVersion: SPDX-2.3
# SPDX-FileCopyrightText: Copyright 2023 Lisa St.John
# SPDX-License-Identifier: GPL-3.0+

import board
import busio
import digitalio
import storage
import supervisor

OnboardLED=digitalio.DigitalInOut(board.LED)
OnboardLED.direction=digitalio.Direction.OUTPUT
EnableSwitch=digitalio.DigitalInOut(board.GP22)
EnableSwitch.direction=digitalio.Direction.INPUT
EnableSwitch.pull=digitalio.Pull.DOWN

UART=busio.UART(board.GP0, board.GP1, baudrate=9600)

def ExtractLatLong(lstr, hemi):
    ret=float(lstr) / 100.0
    if hemi=='S' or hemi=='W':
        ret=-ret
    return ret

class KaiTracker:
    def __init__(self):
        self.last=0
        self.lat=0
        self.lng=0

    def LogPos(self, time, lat, lng):
        if EnableSwitch.value:
            line="Time, {}, lat, {: 2.10f}, long, {: 3.10f}\r\n".format(time, lat, lng)
#            if supervisor.runtime.usb_connected:
#                print(line,end='')
#            else:
            if True:
                try:
                    with open("/kaigpsdata.txt", "a") as fp:
                        fp.write(line)
                        fp.close()
                finally:
                    pass

    def UpdatePos(self, t, lat, lathemi, lng, lnghemi):
        now=int(t.split('.')[0])
        if len(lat)>0 and len(lng)>0:
            if not self.last==now:
                if self.last!= 0:
                    self.LogPos(self.last, self.lat, self.lng)
                self.last=now
                self.lat=ExtractLatLong(lat, lathemi)
                self.lng=ExtractLatLong(lng, lnghemi)
            else:
                self.lat=(self.lat+ExtractLatLong(lat, lathemi))/2.0
                self.lng=(self.lat+ExtractLatLong(lng, lnghemi))/2.0

    def ProcessLines(self, lines):
        for line in lines:
            gps=line.split(',')
            if len(gps[0])>1 and (gps[0][0]=='$'):
                if (gps[0][-3:] == 'GLL'):
                    if len(gps)>5:
                        self.UpdatePos(gps[5], gps[1], gps[2], gps[3], gps[4])
                elif (gps[0][-3:] == 'RMC'):
                    if len(gps)>6:
                        self.UpdatePos(gps[1], gps[3], gps[4], gps[5], gps[6])
                elif (gps[0][-3:] == 'GGA'):
                    if len(gps)>5:
                        self.UpdatePos(gps[1], gps[2], gps[3], gps[4], gps[5])
                else:
                    pass

partial=''
track=KaiTracker()

while True:
    gpsbytes=UART.read(512)
    if gpsbytes is not None:
        OnboardLED.value=True
        lines="".join(chr(c) for c in gpsbytes).split('\n')
        if len(lines)>0:
            lines[0]=partial+lines[0]
            partial=''
            if len(lines[-1])>0:
                if lines[-1][-1] != '\r':
                    partial=lines[-1]
                    lines=lines[:-1]
            else:
                lines=lines[:-1]
            track.ProcessLines(lines)
        OnboardLED.value=False
    else:
        sleep(0.1)
