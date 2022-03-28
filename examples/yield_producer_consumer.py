
def producer(init):
    print('[Producer] init:', init)
    while True:
        init += 1
        print('[Producer] produces 1, now:', init)
        if init >= 5:
            print('[Producer] exit, now:', init)
            init = yield init
            print('[Producer] resume, now:', init)


def consumer(init):
    print('[Consumer] init:', init)
    while True:
        init -= 1
        print('[Consumer] consumes 1, now:', init)
        if init <= 0:
            print('[Consumer] exit, now:', init)
            init = yield init
            print('[Consumer] resume, now:', init)


def scheduler(init):
    p = producer(init)
    now = p.send(None)
    print('[Scheduler] now:', now)
    c = consumer(now)
    now = c.send(None)
    print('[Scheduler] now:', now)
    for _ in range(100):
        now = p.send(now)
        print('[Scheduler] now:', now)
        now = c.send(now)
        print('[Scheduler] now:', now)


scheduler(0)
