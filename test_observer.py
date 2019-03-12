from observers.concrete_subject import ConcreteSubject
from observers.concrete_observer import ConcreteObserver


def test():
    sub1 = ConcreteSubject()
    obs1 = ConcreteObserver()
    obs2 = ConcreteObserver()
    obs1.register_subject(sub1)
    obs2.register_subject(sub1)

    sub1.set_msg('hello')
    sub1.set_msg('hi')
    sub1.set_msg('okok')

    obs2.unregister_subject(sub1)

    sub1.set_msg('hihihihi')


if __name__ == '__main__':
    test()
