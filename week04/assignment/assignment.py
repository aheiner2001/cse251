from datetime import datetime, timedelta
import time
import requests
import json
import threading
from cse251functions import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
CALL_COUNT = 0

# thread that uses requests to retrieve data from the server
class thread_class(threading.Thread):
    def __init__(self, url):  
        threading.Thread.__init__(self)
        self.url = url
        self.data = None

    def run(self):
        global CALL_COUNT 
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(f'You bag, you have failed me once again {self.url}')
        CALL_COUNT += 1


def print_film_details(film, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''
    
    def display_names(title, name_list):
        print('')
        print(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))

    print('-' * 40)
    print(f'Title   : {film["title"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)


def main():
    # Start a timer
    begin_time = time.perf_counter()
    
    print('Starting to retrieve data from the server')

    # Fetch the main API data to get resource URLs
    top_thread = thread_class(TOP_API_URL)
    top_thread.start()
    top_thread.join()
    top_data = top_thread.data

    if not top_data:
        print("Failed to retrieve top data")
        return

    # Retrieve details on film 6
    film_6_url = top_data['films'] + '6'
    film_6_thread = thread_class(film_6_url)
    film_6_thread.start()
    film_6_thread.join()
    film_6_data = film_6_thread.data

    # Setting up category data storage
    categories = ['characters', 'planets', 'starships', 'vehicles', 'species']
    category_data = {category: [] for category in categories}
    
    threads = []

    # Launching threads to fetch all category data
    for category in categories:
        for url in film_6_data[category]:
            thread = thread_class(url)
            threads.append(thread)
            thread.start()

    # Ensuring all threads complete before proceeding
    for thread in threads:
        thread.join()
        category = thread.url.split('/')[-3]
        if 'people' in thread.url:
            category = 'characters'
        
        category_data[category].append(thread.data)

    # Display the retrieved details
    print_film_details(film_6_data, category_data['characters'], category_data['planets'], category_data['starships'], category_data['vehicles'], category_data['species'])

    print(f'There were {CALL_COUNT} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    
    # Checking execution time to ensure proper multithreading
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    
    assert CALL_COUNT == 94, "It should take exactly 94 threads to get all the data"

if __name__ == "__main__":
    main()
    create_signature_file("CSE251W25")
2 