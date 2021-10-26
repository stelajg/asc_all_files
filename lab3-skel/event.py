from threading import enumerate, Event, Thread, Condition


class Master(Thread):
    def __init__(self, max_work, condition):
        Thread.__init__(self, name="Master")
        self.max_work = max_work
        self.condition = condition
        # self.result_available = result_available

    def set_worker(self, worker):
        self.worker = worker

    def run(self):
        for i in range(self.max_work):
            with self.condition:
                # generate work
                self.work = i
                # notify worker
                self.condition.notify()
                # get result
                self.condition.wait()
                if self.get_work() + 1 != self.worker.get_result():
                    print("oops")
                print("%d -> %d" % (self.work, self.worker.get_result()))

    def get_work(self):
        return self.work


class Worker(Thread):
    def __init__(self, terminate, condition):
        Thread.__init__(self, name="Worker")
        self.terminate = terminate
        self.condition = condition

    def set_master(self, master):
        self.master = master

    def run(self):
        while (True):
            with self.condition:
                # wait work
                self.condition.wait()
                if terminate.is_set(): break
                # generate result
                self.result = self.master.get_work() + 1
                # notify master
                self.condition.notify()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    # create shared objects
    terminate = Event()
    condition = Condition()

    # start worker and master
    w = Worker(terminate, condition)
    m = Master(10, condition)
    w.set_master(m)
    m.set_worker(w)
    w.start()
    m.start()

    # wait for master
    m.join()

    # wait for worker
    with condition:
        terminate.set()
        condition.notify_all()
    w.join()

    # print running threads for verification
    print(enumerate())
