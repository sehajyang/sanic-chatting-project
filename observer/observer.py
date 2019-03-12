from abc import abstractmethod


class Observer:

    @abstractmethod
    def update(self, msg):
        pass

    @abstractmethod
    def register_subject(self, subject):
        pass

    @abstractmethod
    def unregister_subject(self, subject):
        pass

    @abstractmethod
    def display(self):
        pass
