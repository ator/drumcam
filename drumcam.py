import getopt, sys

def help():
    print("drumcam - Drum camera recorder")
    print("Usage:")
    print("        drumcam [options]")
    print("Options:")
    print("        -h,--help   Show this help")
    print("        --name      Set the name of the recording")
    print("        --take      Set take number")
    print("        --record    Start recording")

def set_recording_name(name):
    print("Recording name:", name)
    
argument_list = sys.argv[1:]

options = "h"
long_options = ["help", "name=", "take=", "record="]

try:
    arguments, values = getopt.getopt(argument_list, options, long_options)

    argument_functions = {"-h": lambda value: help(),
                          "--help": lambda value: help(),
                          "--name": lambda value: set_recording_name(value)
    }

    if len(arguments) == 0:
        help()

    else:
        for argument, value in arguments:
            argument_functions[argument](value)
        
except getopt.error as err:
    print(str(err))
    help()
