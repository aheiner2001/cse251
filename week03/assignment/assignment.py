'''
Requirements
1. Write a multithreaded program that counts the number of prime numbers 
   between 100,000,000 and 100,370,803.
2. The program should be able to use a variable amount of threads.
3. Each thread should look over an approximately equal number of numbers.
   This means that you need to devise an algorithm that can divide up the
   370,803 numbers "fairly" based on a variable number of threads. 
4. The algorithm should work for 1 to 101 threads.
5. COMMENT every line that you write yourself.
   
Questions:
1. Time to run using 1 thread = 3.61 sec
2. Time to run using 10 threads = 3.5 sec
3. Time to run using 50 threads = 3.55 sec
4. Time to run using 101 threads = 3.57 sec
4. Based on your study of the GIL (see https://realpython.com/python-gil), 
   what conclusions can you draw about the similarity of the times (short answer)?
   >It seems that because of the GIL, which means that only one threas can run at a timem, the time it takes to run the program is similar regardless of the number of threads used.
   >
5. Is this assignment an IO Bound or CPU Bound problem (see https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)?
   > This assignment is CPU bound because the program is doing many compuations with little user input
'''

import math
import threading
import time
from datetime import datetime, timedelta

from cse251functions import *

# Global count of the number of primes found
PRIME_COUNT = 0

# Global count of the numbers examined
NUMBERS_EXAMINED_COUNT = 0

# The number of threads to use (should try 1, 10, 50, and 101 and
# report results above in the questions)
NUMBER_THREADS = 101

def is_prime(n: int):
    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test

   =

    Parameters
    ----------
    ``n`` : int
        Number to determine if prime

    Returns
    -------
    bool
        True if ``n`` is prime.
    """



    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    # Start a timer
    begin_time = time.perf_counter()

    # number to start at
    first_number = 100_000_000

    # interval to check over
    interval = 370_803

    # number to end at
    last_number = first_number + interval



# create partition for ecah thread based on the number of threads
    def partition(first_number, interval, NUMBER_THREADS):

        total_numebrs = first_number + interval
        # finds the number of thread for ech partition
        numbers_per_thread = interval // NUMBER_THREADS
        
        # find the remainer of the interval after dividing by the number of threads
        remainder_for_last_thread =  interval % NUMBER_THREADS

        # this is the stard of the partition
        start = first_number

        # partition list is defined
        partition = []
        
        # for loop to create the partition
        for i in range(NUMBER_THREADS):

            # end of the first partition
            end = start + numbers_per_thread
            
            # the last thread will have the remainder added to the end
            if i == NUMBER_THREADS - 1:
                end += remainder_for_last_thread

            # append to the list
            partition.append((start, end))

            #  change the starting postition so that is was the end of the last partition
            start = end


        return partition
    
            # this function will be run by the thread which will loop though the stard and end of each partition and check if the number is prime
    def count_primes(start, end):
        global PRIME_COUNT
        global NUMBERS_EXAMINED_COUNT
        for i in range(start, end):
            NUMBERS_EXAMINED_COUNT += 1
            if is_prime(i):
                PRIME_COUNT += 1




  
# ceate a list of threads
    threads = []

    # this will store the partitions before we start the threads
    partitions = partition(first_number, interval, NUMBER_THREADS)
    
    # for each stard and end ex. 100000000, 100000100 we will create a thread and runn it with the count_primes function
    for start,end in partitions:
        t  = threading.Thread(target=count_primes, args=(start,end))

        # add the thread to the list
        threads.append(t)
        
        # each thread will be started in this loop
        t.start()


# loop to join all ofthe threads
    for t in threads:
        t.join()
   

    # Use the below code to check and print your results
    assert NUMBERS_EXAMINED_COUNT == 370_803, f"Should check exactly 370,803 numbers, but checked {
        NUMBERS_EXAMINED_COUNT:,}"
    assert PRIME_COUNT == 20_144, f"Should find exactly 20,144 primes but found {
        PRIME_COUNT:,}"

    # Print out summary
    print(f'Numbers processed = {NUMBERS_EXAMINED_COUNT:,}')
    print(f'Primes found = {PRIME_COUNT:,}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")
