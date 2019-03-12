from . import concrete_subject, concrete_observer


def test():
    sub1 = concrete_subject()
    obs = concrete_observer()
    obs.register_subject(sub1)

    sub1.set_msg('hello')
    sub1.set_msg('hi')
    sub1.set_msg('okok')


if __name__ == '__main__':
    test()
