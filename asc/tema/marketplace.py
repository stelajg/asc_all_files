"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Semaphore, RLock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.id_producer = -1
        self.id_carts = -1
        self.producers_list = []  # identifies, for every producers, the remaining space in buffer
        self.market_contains = []  # the market with the lists with the producers products
        self.carts_contains = []  # the list of carts and their products
        self.lock_producers = RLock()
        self.lock_consumers = RLock()
        self.number_of_orders_placed = -1  # used to identify how make consumers are out
        self.consumers_semaphore = Semaphore(0)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.market_contains.append([])
        self.producers_list.append(self.queue_size_per_producer)
        with self.lock_producers:
            self.id_producer += 1
            return self.id_producer

    # every producer has it's own space in the producers_list and
    # market_contains so, here are not need synchronises methods
    # the tuple (Product,status) helps knowing where to return
    # the product and if it's available
    def publish(self, producer_id, product, wait_time_for_making_product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: Int
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :type wait_time_for_making_product: Int
        :param wait_time_for_making_product: the time need to make the product

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if self.producers_list[producer_id] != 0:
            self.market_contains[producer_id].append([product, True])
            self.producers_list[producer_id] -= 1
            self.consumers_semaphore.release()
            time.sleep(wait_time_for_making_product)
            return True
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_consumers:
            self.id_carts += 1
            self.carts_contains.append([])
            return self.id_carts

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.consumers_semaphore.acquire()
        for lists in self.market_contains:
            for item in lists:
                if item[0] is product and item[1] is True:
                    self.carts_contains[cart_id].append(product)
                    with self.lock_consumers:
                        self.producers_list[self.market_contains.index(lists)] += 1
                        item[1] = False
                    return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart

        """
        self.carts_contains[cart_id].remove(product)
        for lists in self.market_contains:
            for item in lists:
                if item[0] is product and item[1] is False:
                    with self.lock_consumers:
                        self.producers_list[self.market_contains.index(lists)] -= 1
                        item[1] = True
        self.consumers_semaphore.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        with self.lock_consumers:
            self.number_of_orders_placed += 1
            return_list = self.carts_contains[cart_id]
            return return_list

    # is used exclusively by producers to identify when to cease
    # making products
    def number_of_orders(self):
        """
        Return False if all the consumers placed their order
        else return true
        """
        with self.lock_producers:
            if self.number_of_orders_placed == self.id_carts:
                return False
            return True
