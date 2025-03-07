'''
Requirements
1. Using multiple threads, put cars onto a shared queue, with one or more thread consuming
   the items from the queue and one or more thread producing the items.
2. The size of queue should never exceed 10.
3. Do not call queue size to determine if maximum size has been reached. This means
   that you should not do something like this: 
        if q.size() < 10:
   Use the blocking semaphore function 'acquire'.
4. The number of cars produced by the manufacturer must equal the number of cars bought by the 
   dealership. Use necessary data objects (e.g., lists) to prove this. There is an assert in 
   main that must be used.
5. COMMENT every line that you write yourself.
   
Questions:
1. How would you define a barrier in your own words?
   >
   >
2. Why is a barrier necessary in this assignment?
   >
   >
'''

import random
import string
import threading
import time
from datetime import datetime, timedelta

from cse251functions import *

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 500

# NO GLOBAL VARIABLES!


class SpaceShip():
    """ This is the SpaceShips class that will be created by the starports """

    # Class Variables
    spaceship_makes = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune',
                       'Pluto')

    spaceship_models = [f"{random.choice(string.ascii_uppercase)}{n}" for n in range(20)]
    spaceship_years = [i for i in range(2100, 2150)]

    def __init__(self):
        # Make a random spaceship
        self.model = random.choice(SpaceShip.spaceship_makes)
        self.make = random.choice(SpaceShip.spaceship_models)
        self.year = random.choice(SpaceShip.spaceship_years)

        # Sleep a little
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the spaceship that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}',flush=True)


class NonBlockingQueue():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)
        if (len(self.items) > MAX_QUEUE_SIZE):
            raise Exception("You have exceeded the size of your space queue!!!\nYou have broken the law and the Solar System Space Force are coming for you...!!!\nYou need to use semaphore.acquire to block when the queue is full, and call semaphore.release after removing a spaceship from the queue.")

    """Will throw an error if called when there are no items (list is empty)"""

    def get(self):
        if (len(self.items) == 0):
            raise Exception("You are trying to pop an item from your queue, but your queue is empty!\nYou must use a semaphore.acquire to block to prevent this from happening. Call semaphore.release after you put a spaceship on the queue, this will unblock the semaphore.acquire.")
        return self.items.pop(0)


class SpaceShipFactory(threading.Thread):
    """ This is a factory.  It will create spaceships and place them on the queue """

    def __init__(self,buyer_count,id, sem_remaining_capacity,sem_spaceship_in_stock, queue, lock,barrier_factory,factory_stats):
        threading.Thread.__init__(self)
        self.spaceships_to_produce = random.randint(
            200, 300)     # Don't change
        self.sem_remaining_capacity = sem_remaining_capacity
        self.sem_spaceship_in_stock = sem_spaceship_in_stock
        self.queue = queue
        self.lock = lock
        self.barrier_factory = barrier_factory
        self.ships_made = 0
        self.id = id
        self.factory_stats = factory_stats
        self.buyer_count =buyer_count

    def run(self):
        # TODO produce the spaceship, the send them to the buyer

        for  i in range(self.spaceships_to_produce):
            self.sem_remaining_capacity.acquire()
            ship  = SpaceShip()
           
            
            # print(f'semaphre remaining capacity acquire {self.queue.size()}')
            self.queue.put(ship)
            with self.lock:
                # how would i haave know to do this ????
                index = min(self.queue.size(), len(self.factory_stats) - 1)
                self.factory_stats[index] += 1

            self.sem_spaceship_in_stock.release()
            # print(f'semaphre stock capacity release {self.queue.size()}')
        print(f'Thread {self.id} calling wait on barrier\n', end="")
        self.barrier_factory.wait()
        if self.id == 0:
            
            for _ in range(self.buyer_count):
                self.queue.put(None)
                self.sem_spaceship_in_stock.release()
        # TODO wait until all of the factories are finished producing spaceships

        # TODO "Wake up/signal" the buyer one more time and send the stop flag.
        # Select one factory to do this (hint: use if factory_id == 0)
        


class SpaceShipBuyer(threading.Thread):
    """ This is a buyer that receives spaceships from the queue """

    def __init__(self,sem_remaining_capacity, sem_spaceship_in_stock, queue, lock, barrier_buyer,buyer_stats):
        threading.Thread.__init__(self)
        self.sem_remaining_capacity = sem_remaining_capacity
        self.sem_spaceship_in_stock = sem_spaceship_in_stock
        self.queue = queue
        self.lock = lock
        self.barrier_buyer = barrier_buyer
        self.buyer_stats = buyer_stats
        self.ships_bought = 0


    def run(self):
        while True:
            # TODO get a spaceship
            self.sem_spaceship_in_stock.acquire()
            # print(f'semaphre stock capacity acquire {self.queue.size()}')
            

            ship = self.queue.get()

            if ship is None:
                break
            
            with self.lock:
                # how would i haave know to do this ????
                index = min(self.queue.size(), len(self.buyer_stats) - 1)
                self.buyer_stats[index] += 1
               
            self.ships_bought +=1


            self.sem_remaining_capacity.release()
           
            # print(f'semaphre remaining capacity release {self.queue.size()}')
       

            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(factory_count, buyer_count):
    """ This function will do a production run with the number of
        factories and buyers passed in as arguments.
    """
    # Start the run
    print(f'Begin production run with {factory_count=} and {buyer_count=}')
    
    # Start a timer
    begin_time = time.perf_counter()

    # TODO Create semaphore(s)
    sem_remaining_capacity = threading.Semaphore(MAX_QUEUE_SIZE)

    sem_spaceship_in_stock = threading.Semaphore(0)

    queue = NonBlockingQueue()

    barrier_factory = threading.Barrier(factory_count)

    barrier_buyer = threading.Barrier(buyer_count)

    # TODO Create queue
    # TODO Create lock(s) -- if needed
    # TODO Create barrier(s)

    buyer_stats = list([0] * buyer_count)

    factory_stats = list([0] * factory_count)

    lock = threading.Lock()

    # TODO create your factories
    factories = []
    for i in range(factory_count):
        factory = SpaceShipFactory(buyer_count,i, sem_remaining_capacity, sem_spaceship_in_stock, queue, lock, barrier_factory,factory_stats)
        factories.append(factory)
        factory.start()

    buyers = []
    for i in range(buyer_count):
        buyer = SpaceShipBuyer(sem_remaining_capacity, sem_spaceship_in_stock, queue, lock, barrier_buyer,buyer_stats)
        buyers.append(buyer)
        buyer.start()  

    for thread in factories:
        thread.join()
    for thread in buyers:
        thread.join()
    

    

    # TODO create your buyers

    # TODO Start all factories

    # TODO Start all buyers

    # TODO Wait for mthem to complete

    run_time = time.perf_counter() - begin_time

    # This function must return the following - only change the variable names, if necessary.
    return (run_time, buyer_stats, factory_stats)


def main():
    """ Main function """

    # Start with (1, 1) to get your code working like the previous assignment, then
    # try adding in different run amounts. You should be able to run the
    # full 7 run amounts.
    # runs = [(1, 1)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, buyers in runs:
        run_time, buyer_stats, factory_stats = run_production(
            factories, buyers)

        print(f'Spaceship Factories : {factories}')
        print(f'Spaceship Buyers    : {buyers}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Factory Stats       : {factory_stats}={sum(factory_stats)}')
        print(f'Buyer Stats         : {buyer_stats}={sum(buyer_stats)}')
        print('')

        # The number of ships produces needs to match the ships sold (this should pass)
        assert sum(buyer_stats) == sum(factory_stats)


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")
