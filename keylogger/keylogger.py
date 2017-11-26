import os
import struct
import sys

# try to guess which event file to use
en = os.popen("grep -E 'Handlers|EV=' /proc/bus/input/devices | grep -B1 'EV=120013' | grep -Eo 'event[0-9]+'").read().\
    rstrip().replace('event', '')

# use the event file indicated, or the guessed if none specified
infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else en)

# struct input_event: long int, long int, unsigned short, unsigned short, unsigned int
# see: https://github.com/torvalds/linux/blob/master/include/uapi/linux/input.h#L24
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

# open file in binary mode
in_file = open(infile_path, "rb")

kbl = 'en_US'

# en_US keyboard layout
KEYS = {
    'en_US': {
        0: '<RESERVED>', 1: '<ESC>', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6',
        8: '7', 9: '8', 10: '9', 11: '0', 12: '-', 13: '=', 14: '<BACKSPACE>',
        15: '<TAB>', 16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u',
        23: 'i', 24: 'o', 25: 'p', 26: '{', 27: '}', 28: '<ENTER>', 29: '<L_CTRL>',
        30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k',
        38: 'l', 39: ';', 40: '\'', 41: '`', 42: '<L_SHIFT>', 43: '\\', 44: 'z',
        45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',', 52: '.',
        53: '/', 54: '<R_SHIFT>', 55: '*', 56: '<L_ALT>', 57: ' ', 58: '<CPSLCK>',
    }
}

event = in_file.read(EVENT_SIZE)

verbose = False
if len(sys.argv) > 2:
    if sys.argv[2] == '-v' or sys.argv[2] == '--verbose':
        verbose = True

candidate = False
while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    if (type != 0 or value != 0) and code == 4:
        # this is probably a key pressed
        candidate = value
    elif type == 1 and value == 1 and candidate:
        # confirmation of a previous candidate
        if verbose:
            print("Event type %u, code %u, value: %s (%u) at %d, %d" %
                  (type, code, KEYS[kbl][candidate], candidate, tv_sec, tv_usec)
            )
        else:
            if candidate == 28:  # handle enter
                sys.stdout.write("\n")
            else:
                sys.stdout.write(KEYS[kbl][candidate])

            # flush output (do not wait until we get a newline to print)
            sys.stdout.flush()

        # clear the last key pressed
        candidate = False

    event = in_file.read(EVENT_SIZE)

in_file.close()
