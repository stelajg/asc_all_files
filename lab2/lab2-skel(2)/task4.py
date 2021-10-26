from threading import Thread, Lock, Semaphore


def run(id_thread, lock_left, lock_right):
    if id_thread == 0:
        lock_left.acquire()
        print(id_thread, "a luat furculita stanga")
        lock_right.acquire()
        print(id_thread, "a luat furculita dreapta")
        lock_left.release()
        lock_right.release()
    else:
        lock_right.acquire()
        print(id_thread, "a luat furculita dreapta")
        lock_left.acquire()
        print(id_thread, "a luat furculita stanga")
        lock_right.release()
        lock_left.release()


def main():
    n = 5
    semaphore_right = Semaphore(n)
    lock_left = Lock()
    thread_list = []
    for i in range(n):
        thread = Thread(target=run, args=(i, lock_left, semaphore_right))
        thread.start()
        thread_list.append(thread)
    for i in range(len(thread_list)):
        thread_list[i].join()


if __name__ == '__main__':
    main()