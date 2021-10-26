"""
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - An infinite loop, which always sends coffees to the distributor
    * User - Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
"""

from threading import Semaphore, Thread, Lock


class Coffee:
    """ Base class """

    def __init__(self):
        pass

    def get_name(self):
        """ Returns the coffee name """
        raise NotImplementedError

    def get_size(self):
        """ Returns the coffee size """
        raise NotImplementedError


class AmericanoCoffee(Coffee):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def get_name(self):
        print("Coffee Americano")

    def get_size(self):
        print("Coffee size = ", self.size)


class EspressoCoffee(Coffee):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def get_size(self):
        print("Coffee size = ", self.size)

    def get_name(self):
        print("Coffee Espresso")


class CappuccinoCoffee(Coffee):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def get_size(self):
        print("Coffee size = ", self.size)

    def get_name(self):
        print("Coffee Cappuccino")


class Distributor:
    def __init__(self):
        self.buffer = []

    def consume(self, coffee, lock):
        lock.acquire()
        print("Was consumed ")
        coffee.get_name()
        self.buffer.pop()
        lock.release()

    def produse(self, coffee, lock):
        lock.acquire()
        print("We put ")
        coffee.get_name()
        self.buffer.append(coffee)
        lock.release()


class CoffeeFactory:
    def __init__(self):
        pass

    def makecoffee(self, i):
        mod = i % 3
        if mod == 0:
            return CappuccinoCoffee(2)
        elif mod == 1:
            return AmericanoCoffee(3)
        else:
            return EspressoCoffee(1)


def producer(sem_prod, sem_consumer, buffer, coffee, lock):
    sem_prod.acquire()
    buffer.produse(coffee, lock)
    sem_consumer.release()


def consumer(sem_prod, sem_consumer, buffer, coffee, lock):
    sem_consumer.acquire()
    buffer.consume(coffee, lock)
    sem_prod.release()


def main():
    print()
    thread_list_consumers = []
    thread_list_producers = []
    lock_consumer = Lock()
    lock_producer = Lock()
    sem_prod = Semaphore(10)
    sem_cons = Semaphore(0)
    buffer = Distributor()
    coffee = CoffeeFactory()
    for i in range(5):
        thread_prod = Thread(target=producer(sem_prod, sem_cons, buffer, coffee.makecoffee(i), lock_producer))
        thread_cons = Thread(target=consumer(sem_prod, sem_cons, buffer, coffee.makecoffee(i), lock_consumer))
        thread_prod.start()
        thread_cons.start()
        thread_list_consumers.append(thread_cons)
        thread_list_producers.append(thread_prod)

    for i in range(len(thread_list_consumers)):
        thread_list_consumers[i].join()

    for i in range(len(thread_list_producers)):
        thread_list_producers[i].join()


if __name__ == '__main__':
    main()
