from observers.observer import Observer


class ConcreteObserver(Observer):
    # def __init__(self, msg, subject):
    #     if subject is None:
    #         print('no subject found')
    #     self.msg = msg
    #     self.subject = subject

    def update(self, msg):
        self.msg = msg
        self.display()

    def register_subject(self, subject):
        print('subscribing ', subject)
        self.subject = subject
        self.subject.register_observer(self)
        print('subscribing success')

    def unregister_subject(self, subject):
        print('unsubscribing ', subject)
        self.subject = subject
        self.subject.remove_observer(self)
        print('unsubscribing success')

    def display(self):
        print(f'msg{self.msg}')
