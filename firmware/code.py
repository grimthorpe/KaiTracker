import board
import busio
import digitalio

OnboardLED=digitalio.DigitalInOut(board.LED)
OnboardLED.direction=digitalio.Direction.OUTPUT
EnableSwitch=digitalio.DigitalInOut(board.
UART=busio.UART(board.GP0, board.GP1, baudrate=9600)

def LogLine(line):
	print(line)

gpsline=''
inGPSdata=False

while True:
	gpsbytes=UART.read(512)
	if gpsbytes is not None:
		OnboardLED.value=True
		for ch in gpsbytes:
			if inGPSdata:
				gpsline+=chr(ch)
				if ch==13:
					LogLine(gpsline)
					inGPSdata=False
			else:
				if ch==36:
					gpsline='$'
					inGPSdata=True
		OnboardLED.value=False
	else:
		sleep(0.1)

