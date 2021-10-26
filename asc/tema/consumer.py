"""
This module represents the Consumer.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread, RLock

lock = RLock()


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__()
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    # for the quantity of every product tries to place them in the specified cart
    # the status variable is used to identify if the action was a success
    def add_command(self, id_cart, product, quantity):
        """
        Makes the add_command from consumer
        :type id_cart: Int
        :param id_cart: the id of the cart in what will be placed the order

        :type product: Product
        :param product: the product that is wanted

        :type quantity: Int
        :param quantity: the quantity of the wanted product
        """
        for _ in range(quantity):
            status = False
            while not status:
                status = self.marketplace.add_to_cart(id_cart, product)
                if not status:
                    time.sleep(self.retry_wait_time)

    # the function is used when the user wants to remove some products
    # from the specified cart
    def remove_command(self, id_cart, product, quantity):
        """
        Makes the remove command from consumer
        :type id_cart: Int
        :param id_cart: the id of the cart in what will be deleted the product

        :type product: Product
        :param product: the product that is wanted removed

        :type quantity: Int
        :param quantity: the quantity of the wanted product
        """
        for _ in range(quantity):
            self.marketplace.remove_from_cart(id_cart, product)

    def run(self):
        for carts in self.carts:
            id_cart = self.marketplace.new_cart()
            for i in carts:
                command = i.get('type')
                if command == 'add':
                    self.add_command(id_cart, i.get('product'), i.get('quantity'))
                else:
                    self.remove_command(id_cart, i.get('product'), i.get('quantity'))

            return_list = self.marketplace.place_order(id_cart)

            for i in enumerate(return_list):
                res = self.kwargs.get('name') + " bought " + format(i[1])
                print(res)
