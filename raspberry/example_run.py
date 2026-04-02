import json
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
ser.write((json.dumps({"cmd": "ping"}) + "\n").encode())
print(ser.readline().decode(errors="ignore").strip())
