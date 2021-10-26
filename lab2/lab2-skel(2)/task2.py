"""
    Basic thread handling exercise:

    Use the Thread class to create and run more than 10 threads which print their name and a random
    number they receive as argument. The number of threads must be received from the command line.

    e.g. Hello, I'm Thread-96 and I received the number 42

"""
import sys
from random import randint, seed
from threading import Lock, Thread


def access(nr, rand_nr, rlock):
    rlock.acquire()
    print("Thread ", nr, " has the number ", rand_nr)
    rlock.release()


def main():
    lock = Lock()
    thread_list = []
    seed()
    print("Put the number of threads")
    n = int(sys.stdin.readline())
    for i in range(n):
        ran = randint(1, 100)
        thread = Thread(target=access,args=(i, ran, lock))
        thread.start()
        thread_list.append(thread)
    for i in range(len(thread_list)):
        thread_list[i].join()


if __name__ == "__main__":
    main()
