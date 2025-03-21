import time
import threading
from cse251functions import *
import random

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5

randomMin = 1  # The minimum time philosophers can eat or think (seconds).
randomMax = 3  # The maximum time philosophers can eat or think (seconds).


class Waiter:
    def __init__(self):
        self.meals = 0
        self.lock = threading.Lock()
        self.all_done = False 


# define the can_eat function and pass in the forks so that the waiter
#  can check to see if they are both there
    def can_eat(self, id, left_fork, right_fork):
        with self.lock:
            if self.meals >= MAX_MEALS:  # Check if total meals are finished.
                self.all_done = True  # Set the flag when meals are done
                return False
            
# i had this probelms of incrementing the meals, so i changd the postion
      # self.meals += 1
        # Try to acquire left fork.

        # i added some print statemenets because i couldn't stop the code from deadlocking
        if left_fork.acquire(timeout=random.randint(randomMin, randomMax)):
            print(f'waiter had checked left fork for {id}')

            # Try to acquire right fork.
            if right_fork.acquire(timeout=random.randint(randomMin, randomMax)):
                print(f'waiter has checked the right fork for: {id} ')
                with self.lock:
                    self.meals += 1
                return True
            else:
                # If right fork isn't available, release the left fork.
                left_fork.release()
                print(f'Philosopher {id} has released the left fork')
                return False
            
             # ADDED IS dinsing complete to check if all the meals are done
    def is_dining_complete(self):
        return self.all_done


# tell the wait that the philosopher is done eating and will release the forks
    def tell_waiter(self, id, left_fork, right_fork):
        print(f'Philosopher {id} is done eating and has told waiter, will now release the forks')
        right_fork.release()
        print(f'Philosopher {id} has released the right fork')
        left_fork.release()
        print(f'Philosopher {id} has released the left fork')

# define the philosopher class and pass in the id, left fork, right fork, and waiter
class Philosopher(threading.Thread):
    def __init__(self, id, left_fork, right_fork, waiter):
        threading.Thread.__init__(self)
        self.id = id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.waiter = waiter
        self.meals = 0
        self.time_eating = 0
        self.time_thinking = 0

    def run(self):
        # ask waiter if they can eat

    # Philosophers need to eat for 1 to 3 seconds when they get both forks.
    # 
 
    # when finished eating, inform waiter
    # think


    # 
        while self.meals < MAX_MEALS and not self.waiter.is_dining_complete():
            # ask waiter if they can eat, if they can eat, eat, if not think
            if self.waiter.can_eat(self.id, self.left_fork, self.right_fork):
                self.eat()
            else:
                self.think()


# eat
    def eat(self):
        print(f'Philosopher {self.id} is eating')

        # find a random time to eat
        time_eating = random.randint(randomMin, randomMax)
        time.sleep(time_eating)

        # increment personal meals
        self.meals += 1
        
        # add to total time
        self.time_eating += time_eating

        print(f"Philosopher {self.id} ate for {time_eating} seconds. Total time eating: {self.time_eating} seconds after {self.meals} meals.")

        # tell the waiter that the philosopher is done eating
        self.waiter.tell_waiter(self.id, self.left_fork, self.right_fork)

        # start thinking
        self.think()

    def think(self):
        print(f'Philosopher {self.id} is thinking')
        time_thinking = random.randint(randomMin, randomMax)
        self.time_thinking += time_thinking
        time.sleep(time_thinking)


def main():
    # Create the waiter.
    waiter_1 = Waiter()

    # Create the forks (semaphores).
    forks = [threading.Semaphore(1) for _ in range(PHILOSOPHERS)]

    # Create PHILOSOPHERS philosophers.
    philosophers = []

    # Add philosophers to the list.
    for i in range(PHILOSOPHERS):
        philosophers.append(Philosopher(i, forks[i], forks[(i + 1) % PHILOSOPHERS], waiter_1))

    # Start the philosophers' threads.
    for philosopher in philosophers:
        philosopher.start()

    # Wait for all philosophers to finish.
    for philosopher in philosophers:
        philosopher.join()

    # Display summary of philosophers' activities.
    print("\nSummary:")
    for philosopher in philosophers:
        print(f"Philosopher {philosopher.id}: Ate {philosopher.meals} times, Spent {philosopher.time_eating}s eating, {philosopher.time_thinking}s thinking.")


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")
