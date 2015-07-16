import time
import inspect

"""
HEADER = '\033[95m' Magenta
OKBLUE = '\033[94m' Blue
OKGREEN = '\033[92m' Green
WARNING = '\033[93m' Yellow
FAIL = '\033[91m' Red
ENDC = '\033[0m'
BOLD = '\033[1m'
"""

# If the stack becomes too complex to figure out a caller we go through and assume the first valid module is the caller.
# This works reasonably well but isn't 100% accurate and will only happen if the caller is a thread.
def print_out(message, color):
    stack = inspect.stack()
    # Interestingly the if statement below is not executed when excepting KeyboardInterrupts. Weird.
    # To prevent a crash we assume the module's name is 'Unknown'
    module = "Unknown"
    if inspect.getmodule(stack[2][0]) == None:
        for i in stack[2:]:
            if inspect.getmodule(i[0]) != None:
                module = inspect.getmodule(i[0]).__name__
    else:
        module = inspect.getmodule(stack[2][0]).__name__
    print("[%s] %s: %s%s\033[0m" % (time.strftime("%x %H:%M:%S"), module, color, message))


def info(message):
    print_out(message, '')


def header(message):
    print_out(message, '\033[95m')


def warning(message):
    print_out(message, '\033[93m')


def error(message):
    print_out(message, '\033[91m')


def success(message, color="green"):
    if color == "green":
        print_out(message, '\033[92m')
    elif color == "blue":
        print_out(message, '\033[94m')


def bold(message):
    print_out(message, '\033[1m')


def underline(message):
    print_out(message, '\033[1m')


