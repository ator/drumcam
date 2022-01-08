from datetime import datetime
import jsonpickle
import npyscreen
import os.path

class Take:
    def __init__(self, recording, number):
        self.recording = recording
        now = datetime.now()
        self.name = now.strftime("%Y%m%d_%H%M%S")
        self.number = number
        self.is_good = False

    def print(self, indent):
        good_bad = "good" if self.is_good else "bad"
        print(f"{indent}Take {self.number} ({good_bad})")
        
    def set_good(self, is_good):
        self.is_good = is_good
        self.save()

    def save(self):
        self.recording.save()
    
class Recording:
    def __init__(self, repository):
        self.repository = repository
        self.name = "Untitled"
        self.takes = []

    def print(self, indent):
        print(f"{indent}Recording {self.name}")
        for take in self.takes:
            take.print(indent + "  ")

    def get_all_takes(self):
        return self.takes
    
    def add_take(self):
        last_take = self.get_last_take()
        if last_take != None:
            last_take_number = last_take.number
        else:
            last_take_number = 0
        take = Take(self, last_take_number + 1)
        self.takes.append(take)
        self.save()
        return take

    def get_last_take(self):
        if len(self.takes) > 0:
            return self.takes[len(self.takes) - 1]
        return None

    def remove_take(self, take):
        self.takes.remove(take)
        self.save()

    def save(self):
        self.repository.save()
        
class Repository:
    filename = ""
    
    def __init__(self):
        self.recordings = []

    def print(self):
        print(f"Repository {self.filename}")
        for recording in self.recordings:
            recording.print("  ")

    def get_all_recordings(self):
        return self.recordings
    
    def get_last_recording(self):
        if len(self.recordings) > 0:
            return self.recordings[len(self.recordings) - 1]
        return None
    
    def add_recording(self):
        recording = Recording(self)
        self.recordings.append(recording)
        self.save()
        return recording

    def remove_recording(self, recording):
        self.recordings.remove(recording)
        self.save()

    def save(self):
        try:
            json = jsonpickle.encode(self)
            file = open(self.filename, "w")
            file.write(json)
            file.close()
        except IOError as err:
            npyscreen.notify_confirm(f"Unable to save to {self.filename}: {str(err)}", title="Save", editw=1)

    @staticmethod
    def load(filename):
        try:
            file = open(filename)
            json = file.read()
            config = jsonpickle.decode(json)
            file.close()
            return config
        except IOError as err:
            npyscreen.notify_confirm(f"Unable to load from {self.filename}: {str(err)}", title="Save", editw=1)
    
    @staticmethod
    def load_or_create(filename):
        if os.path.isfile(filename):
            repository = Repository.load(filename)
        else:
            repository = Repository()
        repository.filename = filename
        return repository
