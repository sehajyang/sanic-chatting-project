from observer.subject import Subject


class ConcreteObserver(Subject):
    def __init__(self):
        super(ConcreteObserver, self).__init__()
        self._observer = []
        self.msg = ""

    def register_observer(self, observer):
        if observer in self._observer:
            return "already exist observer"
        self.register_observer(observer)
        return "register success"

    def remove_observer(self, observer):
        if observer in self._observer:
            self._observer.remove(observer)
            return "remove success"
        return "observer not exist"

    def notify_observer(self):
        for observer in self._observer:
            observer.update(self.msg)

    def msg_changed(self):
        self.notify_observer()

    def set_msg(self, msg):
        self.msg = msg
        self.msg_changed()




