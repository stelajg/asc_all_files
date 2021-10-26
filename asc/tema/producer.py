"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__()
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    # tries to place the quantity of every product in the market_place
    # the status variable is used to identify if the action was a success
    # and if in the market_place are active consumers
    def helper_run(self, producer_id, command_info):
        """
        publish the product
        :type producer_id: Int
        :param producer_id: the producer_id that will make the publishing

        :type command_info: Tuple
        :param command_info: contains the product, the number of publish
        operations and the time needed to make the product

        """
        for _ in range(command_info[1]):
            status = False
            while not status:
                status = self.marketplace.publish(producer_id, command_info[0], command_info[2])
                if not status:
                    time.sleep(self.republish_wait_time)
                if not self.marketplace.number_of_orders():
                    status = True

    def run(self):
        id_prod = self.marketplace.register_producer()
        time_to_run = True
        while time_to_run:
            for i in self.products:
                self.helper_run(id_prod, i)
            time_to_run = self.marketplace.number_of_orders()
