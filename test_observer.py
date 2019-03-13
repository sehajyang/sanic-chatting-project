from observers.subject import Subject
from observers.observer import Observer



def test():
    sub1 = Subject()
    obs1 = Observer()
    obs2 = Observer()
    obs1.register_subject(sub1)
    obs2.register_subject(sub1)

    sub1.set_msg('hello')
    sub1.set_msg('hi')
    sub1.set_msg('okok')

    obs2.unregister_subject(sub1)

    sub1.set_msg('hihihihi')


if __name__ == '__main__':
    test()
