import serial
import time
import pprint


# The max values depend on where
# you homed (0,0,0).
max_x = 407.5
max_y = 295
tool_step_over = 10
tool_step_down = .01
feed_speed = 750
com_port = 'COM7'
baud_rate = 115200
grbl_init_delay = 2
G_spindle_start = 'M03'
G_spindle_stop = 'M05'
z_safe_distance_mm = 5

# Open grbl serial port
s = serial.Serial(com_port,baud_rate)

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(grbl_init_delay)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input


def start_code ():
        pprint("WIP: Start Code")


def start_spindle ():
    print ('Sending: ' + l, s.write(+ '\n'))

def next_column (x,y,z,f):
    global max_x,max_y,tool_step_over
    if x < max_x and y < max_y:
        pprint ("Within Limits")

# Stream g-code to grbl
feed_speed = "F1000"
go_to_x0_y0 = "G0 X0 Y0"
command_list = list((feed_speed,go_to_x0_y0))



for index,value in command_list:
    print ('Sending: ' + l, s.write(+ '\n')) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print (' : ' + grbl_out.strip())

# Wait here until grbl is finished to close serial port and file.
input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
s.close()