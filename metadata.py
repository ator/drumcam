import jsonpickle
import os.path

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

class Repository:

    def __init__(self, filename):
        self.filename = filename
        self.recordings = []

    def print(self):
        print("Repository:", self.filename)
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
            return Repository.load(filename)
        repository = Repository(filename)
        repository.save()
        return repository
