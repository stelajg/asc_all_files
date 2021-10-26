from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import current_thread
import time, random

data = ["lab1", "lab2", "lab3"]


def modify_msg(msg):
    # time.sleep(random.randint(1, 5))
    return "Completed: [" + msg.title() + "] in thread " + str(current_thread())


def main():
    with ThreadPoolExecutor(max_workers=310) as executor:
        results = executor.map(modify_msg, data)

    for result in results:
        print(result)


if __name__ == '__main__':
    main()

