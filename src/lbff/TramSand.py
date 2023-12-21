import glob
import sys
import serial
import time
import pprint
from threading import Event

# NOTE

# Machine [WorK] Origin Coordinates with sander at surface
#   X:  -411.925 [80.287]
#   Y:  -284.438 [294.613]
#   Z:  -98.925 [0.000]


# The max values depend on where
# you homed (0,0,0).
max_x = 407.5
max_y = 295
tool_step_over = 10
tool_step_down = 0.01
feed_speed = 750
com_port = "COM7"
baud_rate = 115200
grbl_init_delay = 2
z_safe_distance_mm = 5


class GRBL_Commands(object):
    _instance = None

    def __init__(self):
        self.spindle_start = "M03"
        self.spindle_stop = "M05"
        self.set_absolute_movement = "G90"
        self.set_relative_movement = "G91"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GRBL_Commands, cls).__new__(cls)
        return cls._instance


def serial_ports():
    """Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


import serial.tools.list_ports


def list_serial_ports():
    ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))


def get_port_name(vendor_id="", product_id=""):
    for port in serial.tools.list_ports.comports():
        pprint.pprint(vars(port))
        if port.vid == vendor_id and port.pid == product_id:
            return port.name


def send_wake_up(serial_connection):
    """Sends a wakeup to the controller

    :raises NoException:
        nothing
    :returns:
        nothing
    """
    # Wake up
    # Hit enter a few times to wake the Printrbot
    serial_connection.write(str.encode("\r\n\r\n"))
    time.sleep(grbl_init_delay)  # Wait for Printrbot to initialize
    serial_connection.flushInput()  # Flush startup text in serial input


def wait_for_movement_completion(ser, cleaned_line):
    Event().wait(1)

    if cleaned_line != "$X" or "$$":
        idle_counter = 0

        while True:
            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode("?" + "\n")
            ser.write(command)
            grbl_out = ser.readline()
            grbl_response = grbl_out.strip().decode("utf-8")

            if grbl_response != "ok":
                if grbl_response.find("Idle") > 0:
                    idle_counter += 1

            if idle_counter > 10:
                break
    return


def start_code():
    pprint("WIP: Start Code")


def start_spindle():
    print("Sending: " + G.spindle_start, s.write(+"\n"))


def next_column(x, y, z, f):
    global max_x, max_y, tool_step_over
    if x < max_x and y < max_y:
        pprint("Within Limits")


G = GRBL_Commands()

# Stream g-code to grbl
set_feed_speed = "F" + str(feed_speed)
move_to_Z_safe = "G0 Z" + str(z_safe_distance_mm)
go_to_x_y_origin = "G0 X0 Y0"


if __name__ == "__main__":
    print("And so it begins!")

    # Open grbl serial port
    port_name = get_port_name(6790, 29987)
    print("CNC Port Name:", port_name)
    if port_name == None:
        raise (ValueError)
    s = serial.Serial(port_name, baud_rate)

    # Wake up grbl
    send_wake_up(s)

    command_list = list(
        (
            G.set_relative_movement,
            move_to_Z_safe,
            G.spindle_start,
            set_feed_speed,
            go_to_x_y_origin,
        )
    )
    command_list = list((G.spindle_start, G.spindle_stop))

    for command in command_list:
        print("Command: ", command)
        print(
            "Sending: ", command, s.write((command + "\n").encode())
        )  # Send g-code block to grbl

        wait_for_movement_completion(s, command)

        grbl_out = s.readline()  # Wait for grbl response with carriage return
        print(" : ", grbl_out.strip().decode("utf-8"))

    # Wait here until grbl is finished to close serial port and file.
    input("  Press <Enter> to exit and disable grbl.")

    # Close the serial port
    s.close()
