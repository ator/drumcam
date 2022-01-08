import getopt
import metadata
import npyscreen
import sys
import ui

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", ui.RecordingListDisplay)
        self.addForm("EDIT_RECORDING", ui.TakeListDisplay)
#        self.addForm("EDIT_TAKE", ui.EditTakeDisplay)

def load_repository(repository_filename):
    return metadata.Repository.load_or_create(repository_filename)
    
def print_help():
    print("drumcam - Drum camera recorder")
    print("Usage:")
    print("        drumcam [options]")
    print("Options:")
    print("        -h,--help          Show this help")
    print("        --repo <filename>  Use <filename> as metadata repository (defaults to .repo/drumcam.repo)")
    print("        --print            Print out the metadata repository contents")

def load_arguments():
    argument_list = sys.argv[1:]
    
    options = "h"
    long_options = ["help", "repo=", "print"]
    
    repository_filename = ".repo/drumcam.repo"
    print_repository = False
    
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        
        for argument, value in arguments:
            if argument == "-h" or argument == "--help":
                print_help()
                sys.exit()
                
            elif argument == "--repo":
                repository_filename = value
                
            elif argument == "--print":
                print_repository = True
                
        return repository_filename, print_repository
        
    except getopt.error as err:
        print(str(err))
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    repository_filename, print_repository = load_arguments()
    repository = load_repository(repository_filename)
    if print_repository:
        repository.print()
    else:
        app = App()
        app.repository = repository
        app.run()
