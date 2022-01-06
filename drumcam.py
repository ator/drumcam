from datetime import datetime
import getopt
import sys
import metadata

def print_help():
    print("drumcam - Drum camera recorder")
    print("Usage:")
    print("        drumcam [options]")
    print("Options:")
    print("        -h,--help          Show this help")
    print("        --repo <filename>  Use <filename> as metadata repository (defaults to drumcam.repo)")
    print("        --print            Print out the metadata repository contents")

def load_arguments():
    argument_list = sys.argv[1:]
    
    options = "h"
    long_options = ["help", "repo=", "print"]
    
    repository_filename = "drumcam.repo"
    print_repository = False
    
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        
        for argument, value in arguments:
            if argument == "-h" or argument == "--help":
                print_help()
                sys.exit()
                
            elif argument == "--repository":
                repository_filename = value
                
            elif argument == "--print":
                print_repository = True

        return repository_filename, print_repository
    
    except getopt.error as err:
        print(str(err))
        print_help()
        sys.exit(1)

repository_filename, print_repository = load_arguments()

repository = metadata.Repository.load_or_create(repository_filename)

if print_repository:
    repository.print()
    
else:
    recording = repository.get_last_recording()
    if recording == None:
        now = datetime.now()
        name = now.strftime("%Y%m%d_%H%M%S")
        recording = repository.new_recording(name)
        
    take = recording.new_take()
    take.toggle_good()
    
    repository.save()
