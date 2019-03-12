class Subject:
    def __init__(self):
        self.observer = []

    def register_observer(self, observer):
        self.observer.append(observer)

    def remove_observer(self, observer):
        self.observer.remove(observer)

    def notify_observer(self, info):
        for obs in self.observer:
            obs.msg = info

