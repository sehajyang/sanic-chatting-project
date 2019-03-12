from abc import ABCMeta, abstractmethod


class DisplayData:
    __metaclass__ = ABCMeta

    @abstractmethod
    def display(self):
        pass
