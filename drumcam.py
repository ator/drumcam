from datetime import datetime
import getopt
import jsonpickle
import os.path
import sys

class Take:
    def __init__(self, number):
        self.number = number
        self.is_good = False

    def print(self):
        print("Take", self.number, "(good)" if self.is_good else "(bad)")
        
    def toggle_good(self):
        self.is_good = not self.is_good
    
class Recording:

    def __init__(self, name):
        self.name = name
        self.takes = []

    def print(self):
        print("Recording:", self.name)
        for take in self.takes:
            take.print()
            
    def new_take(self):
        last_take = self.get_last_take()
        if last_take != None:
            last_take_number = last_take.number
        else:
            last_take_number = 0
        take = Take(last_take_number + 1)
        self.takes.append(take)
        return take

    def get_last_take(self):
        if len(self.takes) > 0:
            return self.takes[len(self.takes) - 1]
        return None

    def remove_take(self, take):
        self.takes.remove(take)

class Metadata:

    def __init__(self, filename):
        self.filename = filename
        self.recordings = []

    def print(self):
        print("Metadata:", self.filename)
        for recording in self.recordings:
            recording.print()
        
    def get_last_recording(self):
        if len(self.recordings) > 0:
            return self.recordings[len(self.recordings) - 1]
        return None
    
    def new_recording(self, name):
        recording = Recording(name)
        self.recordings.append(recording)
        return recording

    def remove_recording(self, recording):
        self.recordings.remove(recording)

    def save(self):
        try:
            json = jsonpickle.encode(self)
            file = open(self.filename, "w")
            file.write(json)
            file.close()
        except IOError as err:
            print(str(err))
            print("Unable to save config to", self.filename)

    @staticmethod
    def load(filename):
        try:
            file = open(filename)
            json = file.read()
            config = jsonpickle.decode(json)
            file.close()
            return config
        except IOError as err:
            print(str(err))
            print("Unable to load config from", filename)
    
    @staticmethod
    def load_or_create(filename):
        if os.path.isfile(filename):
            return Metadata.load(filename)
        metadata = Metadata(filename)
        metadata.save()
        return metadata
    
def print_help():
    print("drumcam - Drum camera recorder")
    print("Usage:")
    print("        drumcam [options]")
    print("Options:")
    print("        -h,--help             Show this help")
    print("        --metadata <filename> Use <filename> to store metadata (defaults to drumcam.metadata)")
    print("        --print               Print out the metadata contents")

argument_list = sys.argv[1:]

options = "h"
long_options = ["help", "metadata=", "print"]

metadata_filename = "drumcam.metadata"
print_metadata = False

try:
    arguments, values = getopt.getopt(argument_list, options, long_options)

    for argument, value in arguments:
        if argument == "-h" or argument == "--help":
            print_help()
            sys.exit()
            
        elif argument == "--metadata":
            metadata_filename = value

        elif argument == "--print":
            print_metadata = True
    
except getopt.error as err:
    print(str(err))
    print_help()
    sys.exit(1)
    
metadata = Metadata.load_or_create(metadata_filename)

if print_metadata:
    metadata.print()
    
else:
    recording = metadata.get_last_recording()
    if recording == None:
        now = datetime.now()
        name = now.strftime("%Y%m%d_%H%M%S")
        recording = metadata.new_recording(name)
        
    take = recording.new_take()
    take.toggle_good()
        
    metadata.save()
