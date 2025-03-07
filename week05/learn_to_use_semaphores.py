import os
import random
import sys
import threading
import time
from datetime import datetime, timedelta



class Food:

    kind = ('Apple', 'Chocolate', 'Sugar', 'Bacon', 'Bread', 'Strawberry', 'Orange', 'Banana',
            'Celery', 'Beef', 'Chicken', 'Peanut Butter')

    def __init__(self):
        self.choice = random.choice(Food.kind)

        # Takes some time to prepare food
        time.sleep(random.uniform(0.1, 0.25))

        print(f'putting {self.choice} on the table\n', end="")

    def __str__(self) -> str:
        return self.choice


class Queue251():

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)
    
    def size(self):
        return len(self.items)


class Feeder(threading.Thread):
    def __init__(self,semaphore_remaining_capacity, semaphore_food_on_table, table_queue):
        threading.Thread.__init__(self )
        # TODO - add parameters to constructor and create attributes
        self.semaphore_remaining_capacity = semaphore_remaining_capacity
        self.semaphore_food_on_table = semaphore_food_on_table
        self.table_queue = table_queue
        self.food_to_make = 100
        self.food_made = 0
        

    def run(self):
        # Loop over amount of food to make
        for _ in range(self.food_to_make):
        
            # TODO - use a semaphore to prevent putting too much food in queue (table)
            self.semaphore_remaining_capacity.aquire()
            
            
            # TODO - put food on queue (table), increment food made counter
            food = Food()
            self.table_queue.put(food)
            self.food_made +=1

            # TODO - signal to eater that food has been placed on table
            self.semaphore_food_on_table.release()

        # TODO - after adding all food, signal to eater that there is no more food
       
        self.table_queue.put(None)
        


class Eater(threading.Thread):

    def __init__(self,semaphore_remaining_capacity,semaphore_food_on_table, table_queue):
        threading.Thread.__init__(self)
        # TODO - add parameters to constructor and create attributes
        self.semaphore_remaining_capacity = semaphore_remaining_capacity
        self.semaphore_food_on_table = semaphore_food_on_table
        self.table_queue = table_queue
        self.food_eaten = 0
    

    def run(self):
        while True:

            # TODO - using a semaphore, prevent removing item from an empty queue
            self.semaphore_food_on_table.aquire()
            
            # TODO - get food from queue
            food = self.table_queue.get()
            if food == None:
                break
            self.food_eaten +=1
            # TODO - if item from queue is Sentinel, then break; else increment food ate counter
            
            # TODO - signal to feeder to put more food on table
            self.semaphore_remaining_capacity.release()

            # Need some time to digest (leave this)
            time.sleep(random.uniform(0.01, 0.1))


def main(number_of_eaters, number_of_feeders):

    print(
        f'\n### Starting with {number_of_eaters} eater(s) and {number_of_feeders} feeder(s) ###\n')

    # TODO - create a max table size (i.e., maximum size of queue), call it table_queue
    TABLE_SIZE = 10

    # TODO - create semaphore to represent remaining capacity on table
    semaphore_remaining_capacity = threading.Semaphore(TABLE_SIZE)

    # TODO - create semaphore to represent if table has food on it
    semaphore_food_on_table = threading.Semaphore(0)

    # TODO - Create a place to put food, a table/queue
    table_queue = Queue251()
    

    
    feeder_t = Feeder(semaphore_remaining_capacity,semaphore_food_on_table, table_queue)
    feeder_t.start()

    eater_t = Eater(semaphore_remaining_capacity,semaphore_food_on_table, table_queue)
    eater_t.start()
    # TODO - join threads to wait for eating to be done

    feeder_t.join()
    eater_t.join()



    print(f'Maximum number of food on table = {table_queue.get_max_size()}')
    assert table_queue.get_max_size(
    ) <= TABLE_SIZE, f'table max size is {table_queue.get_max_size()} but should be less than or equal to {TABLE_SIZE}'

    # eaten = feeder_t.food_made

    # made = eater_t.food_eaten

    print(f'Total amount of food made = {made}')
    print(f'Total amount of food eaten = {eaten}')

    assert made == eaten, f'Total amount of food made is {
        made}, which does not equal amount of food eaten of {eaten}'


if __name__ == '__main__':
    main(1, 1)
    print('Exiting program')
