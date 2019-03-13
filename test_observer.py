from room.room import Room



def test():
    sub1 = Room()
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
