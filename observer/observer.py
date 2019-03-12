class Observer:
    def __init__(self):
        self.subscriber = []
        self.msg = ""

    def notify(self):
        for sub in self.subscriber:
            sub.msg = self.msg

    def register(self, observer):
        self.subscriber.append(observer)

    def remove(self, observer):
        self.subscriber.remove(observer)
