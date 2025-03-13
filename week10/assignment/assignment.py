'''
Requirements
1. Create a multiprocessing program that reads in files with defined tasks to perform.
2. The program should use a process pool per task type and use apply_async calls with callback functions.
3. The callback functions will store the results in global lists based on the task to perform.
4. Once all 4034 tasks are done, the code should print out each list and a breakdown of 
   the number of each task performed.
5. COMMENT every line that you write yourself.
   
Questions:
1. How many processes did you specify for each pool:
   >Finding primes:4
   >Finding words in a file: 10 
   >Changing text to uppercase: 4
   >Finding the sum of numbers:4
   >Web request to get names of Star Wars people:10
   
   >How do you determine these numbers: My computer has 8 cores, so I decided to use half of the cores for each pool. and i tried to use 16 for the io bound but it was avergagin around 8 sec, so i went down to 10 which seems to be the fastest.
   
2. Specify whether each of the tasks is IO Bound or CPU Bound?
   >Finding primes: CPU BOUnd
   >Finding words in a file: IO BOUND
   >Changing text to uppercase: CPU BOUND
   >Finding the sum of numbers:CPU BOUND
   >Web request to get names of Star Wars people: IO BOUND
   
3. What was your overall time, with:
   >one process in each of your five pools:  34.5 seconds
   >with the number of processes you show in question one:  6.68 seconds
'''

import glob
import json
import math
import multiprocessing as mp
import os
import time
from datetime import datetime, timedelta
from cse251functions import *

import numpy as np
import requests

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
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


def task_prime(value):
    # return with the is prime function
    return is_prime(value)


def task_word(word):
    # open words.txt and search for the word return if the wrod is found
    
    with open('words.txt') as f:
        words = f.read().splitlines()
        for w in words:
            if word in w:
                return w
        return None
    


def task_upper(text):
    # returns the uppercase of the text
    return text.upper()

def task_sum(start_value, end_value):
    # the sum funciton add them up without having to loop through them all
    return sum(range(start_value, end_value + 1))

def task_name(url):
#    returns the name
    return requests.get(url).json()['name']

def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    begin_time = time.time()
    count = 0
    
    # created the list for the pools
    pools = []

    # each pool in created
   
    prime_pool = mp.Pool(processes=4)
    word_pool = mp.Pool(processes=10)
    upper_pool = mp.Pool(processes=4)
    sum_pool = mp.Pool(processes=4)
    name_pool = mp.Pool(processes=10)    

    # append pools to a list
    pools.append(prime_pool)
    pools.append(word_pool) 
    pools.append(upper_pool)
    pools.append(sum_pool)
    pools.append(name_pool)




    # The below code is example code to show you the logic of what you are supposed to do.
    # Remove it and replace with using process pools with apply_async calls.
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']

        #  i modified the code to use async programming
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(func=task_prime, args=(task['value'],), callback=result_primes.append)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(func=task_word, args=(task['word'],), callback=result_words.append)
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(func=task_upper, args=(task['text'],), callback=result_upper.append)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(func=task_sum, args=(task['start'], task['end']), callback=result_sums.append)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(func=task_name, args=(task['url'],), callback=result_names.append)
        else:
            print(f'Error: unknown task type {task_type}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # start pools and block until they are done before trying to print
    for pool in pools:
        pool.close()
        pool.join()
        

  
    def print_list(lst):
        for item in lst:
            print(item)
        print(' ')

    print('-' * 80)
    print(f'Primes: {len(result_primes)}')
    print_list(result_primes)

    print('-' * 80)
    print(f'Words: {len(result_words)}')
    print_list(result_words)

    print('-' * 80)
    print(f'Uppercase: {len(result_upper)}')
    print_list(result_upper)

    print('-' * 80)
    print(f'Sums: {len(result_sums)}')
    print_list(result_sums)

    print('-' * 80)
    print(f'Names: {len(result_names)}')
    print_list(result_names)

    print(f'Number of Primes tasks: {len(result_primes)}')
    print(f'Number of Words tasks: {len(result_words)}')
    print(f'Number of Uppercase tasks: {len(result_upper)}')
    print(f'Number of Sums tasks: {len(result_sums)}')
    print(f'Number of Names tasks: {len(result_names)}')
    print(f'Finished processes {count} tasks = {time.time() - begin_time}')


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")
