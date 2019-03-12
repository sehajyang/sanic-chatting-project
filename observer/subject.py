from abc import ABCMeta, abstractmethod


class Subject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass
