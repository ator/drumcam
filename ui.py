import curses
import npyscreen

class TakeList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TakeList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_take,
            "^D": self.when_delete_take,
            "^G": self.when_set_good,
            "^B": self.when_set_bad,
            curses.ascii.ESC: self.when_exit
        })

    def display_value(self, take):
        good_bad = "good" if take.is_good else "bad"
        return f"{take.number}: {take.name} ({good_bad})"

#    def actionHighlighted(self, act_on_this, keypress):
#        self.parent.parentApp.getForm('EDIT_TAKE').value = act_on_this
#        self.parent.parentApp.switchForm('EDIT_TAKE')

    def when_add_take(self, *args, **keywords):
        take = self.parent.add_take()
#        self.parent.parentApp.getForm('EDIT_TAKE').value = take
#        self.parent.parentApp.switchForm('EDIT_TAKE')

    def when_delete_take(self, *args, **keywords):
        self.parent.remove_take(self.values[self.cursor_line])

    def when_set_good(self, *args, **keywords):
        self.parent.set_good(self.values[self.cursor_line])

    def when_set_bad(self, *args, **keywords):
        self.parent.set_bad(self.values[self.cursor_line])

    def when_exit(self, *args, **keywords):
        self.parent.exit()

class TakeListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TakeList
    def beforeEditing(self):
        self.update_list()
        self.wStatus1.value = f"{self.value.name}"
        self.wStatus2.value = "^A=Add, ^D=Delete, ^G=Set Good, ^B=Set Bad, ESC=Exit"

    def update_list(self):
        self.wMain.values = self.value.get_all_takes()
        self.wMain.display()

    def add_take(self):
        take = self.value.add_take()
        self.update_list()
        return take

    def remove_take(self, take):
        if npyscreen.notify_yes_no(f"Are you sure you want to delete take {take.name}?", title="Delete Take"):
            self.value.remove_take(take)
            self.update_list()

    def set_good(self, take):
        take.set_good(True)
        self.update_list()

    def set_bad(self, take):
        take.set_good(False)
        self.update_list()
        
    def exit(self):
        self.parentApp.switchForm("MAIN")

class RecordingList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordingList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_recording,
            "^D": self.when_delete_recording,
            curses.ascii.ESC: self.when_exit
        })

    def display_value(self, recording):
        return recording.name

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDIT_RECORDING').value = act_on_this
        self.parent.parentApp.switchForm('EDIT_RECORDING')

    def when_add_recording(self, *args, **keywords):
        recording = self.parent.add_recording()
        self.parent.parentApp.getForm('EDIT_RECORDING').value = recording
        self.parent.parentApp.switchForm('EDIT_RECORDING')

    def when_delete_recording(self, *args, **keywords):
        self.parent.remove_recording(self.values[self.cursor_line])

    def when_exit(self, *args, **keywords):
        self.parent.exit()
        
class RecordingListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = RecordingList
    def beforeEditing(self):
        self.update_list()
        self.wStatus1.value = "Recordings"
        self.wStatus2.value = "^A=Add, ^D=Delete, ESC=Exit"

    def update_list(self):
        self.wMain.values = self.parentApp.repository.get_all_recordings()
        self.wMain.display()

    def add_recording(self):
        recording = self.parentApp.repository.add_recording()
        self.update_list()
        return recording

    def remove_recording(self, recording):
        if npyscreen.notify_yes_no(f"Are you sure you want to delete recording {recording.name}?", title="Delete Recording", editw=1):
            self.parentApp.repository.remove_recording(recording)
            self.update_list()

    def exit(self):
        if npyscreen.notify_yes_no("Are you sure?", title="Exit", editw=2):
            self.parentApp.switchForm(None)
