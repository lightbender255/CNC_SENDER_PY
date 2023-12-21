import serial
import time

port = "COM6"
baud = 115200
grbl_file = "TramSand.nc"

# Open grbl serial port
s = serial.Serial(port, baud)

# Open g-code file
f = open(grbl_file, "r")

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)  # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
for line in f:
    l = line.strip()  # Strip all EOL characters for consistency
    print("Sending: " + l, s.write(l + "\n"))  # Send g-code block to grbl
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    print(" : " + grbl_out.strip())

# Wait here until grbl is finished to close serial port and file.
input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
f.close()
s.close()
