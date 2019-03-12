

class Subject:
    def __init__(self):
        self._observer = []
        self.msg = ""

    def register_observer(self, observer):
        if observer in self._observer:
            return False
        self._observer.append(observer)
        return True

    def remove_observer(self, observer):
        if observer in self._observer:
            self._observer.remove(observer)
            return True
        return False

    def notify_observer(self):
        for observer in self._observer:
            observer.update(self.msg)

    def msg_changed(self):
        self.notify_observer()

    def set_msg(self, msg):
        self.msg = msg
        self.msg_changed()
