'''
Requirements
1. Create a multiprocessing program that connects the processes using Pipes.
2. Create a process from each of the following custom process classes, 
   Marble_Creator, Bagger, Assembler, and Wrapper.
3. The Marble_Creator process will send a marble to the Bagger process using
   a Pipe.
4. The Bagger process will create a Bag object with the required number of
   marbles. 
5. The Bagger process will send the Bag object to the Assembler using a Pipe.
6. The Assembler process will create a Gift object and send it to the Wrapper
   process using a Pipe.
7. The Wrapper process will write to a file the current time followed by the 
   gift string.
8. The program should not hard-code the number of marbles, the various delays,
   nor the bag count. These should be obtained from the settings.txt file.
9. COMMENT every line that you write yourself.
   
Questions:
1. Why can you not use the same pipe object for all the processes (i.e., why 
   do you need to create three different pipes)?
   >Because the pipers would then pass information to the wrong process
   
2. Compare and contrast pipes with queues (i.e., how are the similar or different)?
   >It's nice how they don't need semaphores to lock the data
   
'''

import datetime
import json
import multiprocessing as mp
import os
import random
from datetime import datetime
import time
from cse251functions import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

# add the other arguments to the __init__ mehtod
    def __init__(self,pipe_send, marble_count, delay):
        mp.Process.__init__(self)

        
        self.colors = Marble_Creator.colors
        self.pipe_send = pipe_send



    # marle count and delay are the arguments that are passed in
        self.marble_count = marble_count
        self.delay = delay

     

    def run(self):

# while there are marbles to process
# collect enough marbles for a bag
# send the bag to the assembler
# sleep the required amount
# tell the assembler that there are no more bags
        while self.marble_count > 0:
            marble = random.choice(self.colors)
            
            self.pipe_send.send(marble)
         
            
            self.marble_count -= 1
            time.sleep(self.delay)
        self.pipe_send.send(None)



        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
# add the other arguments to the __init__ mehtod
    def __init__(self, pipe_receive, pipe_send, bag_count, delay):
        mp.Process.__init__(self)
        self.pipe_receive = pipe_receive
        self.pipe_send = pipe_send
        self.bag_count = bag_count
        self.delay = delay
    

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        
        '''
        # while there are marbles to process

        while True:
                
    #   create bag, loop through range of ba count, add marble to bag, send the filled bag, sleep the required amount
                bag = Bag()
                for _ in range(self.bag_count):
                    marble = self.pipe_receive.recv()  # Receive a marble
                
                    if marble is None:
                        self.pipe_send.send(None)  # Pass the termination signal
                        return  # Exit process

                    bag.add(marble)  # Add marble to the bag

                self.pipe_send.send(bag)  # Send the filled bag
            
                time.sleep(self.delay)  
                self.pipe_receive.close()
                self.pipe_send.close()
                    


        

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, pipe_receive, pipe_send, delay):
        mp.Process.__init__(self)
        self.pipe_receive = pipe_receive
        self.pipe_send = pipe_send
        self.delay = delay
    

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        # while there are bags, add large marbel to the box aan send the gift to the wrapper
        while True:
            bag = self.pipe_receive.recv()
           
            if bag is None:
                self.pipe_send.send(None)
                break
            large_marble = random.choice(Assembler.marble_names)

            gift = Gift(large_marble, bag)
            self.pipe_send.send(gift)
            
            time.sleep(self.delay)

         


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, pipe_receive, delay, total_gifts):
        mp.Process.__init__(self)
        self.pipe_receive = pipe_receive
        self.delay = delay
        self.total_gifts = total_gifts

    def run(self):
        with open(BOXES_FILENAME, 'a') as file:  # Open file in append mode
            while True:
                gift = self.pipe_receive.recv()
                if gift is None:
                    break
                self.total_gifts.value += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f'{timestamp} - {gift}\n')  # Write the timestamp and gift
                time.sleep(self.delay)


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # Load settings file

    settings = load_json_file(CONTROL_FILENAME)
    print(settings)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

   
    # creator -> bagger -> assembler -> wrapper
    # 
# Created three pipes to send between the different senders and receivers
    pipe_creator_to_bagger_send, pipe_bagger_from_creator_receive = mp.Pipe()
    pipe_bagger_to_assembler_send, pipe_assembler_from_bagger_receive = mp.Pipe()
    pipe_assembler_to_wrapper, pipe_wrapper_from_assembler_receive = mp.Pipe()

    # I had to look this up, but i remember us talking about it in class
    # manager is used to share the total gifts between the processes
    manager = mp.Manager()
    total_gifts = manager.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    print('Create the processes')

  

    # Each process is instantiated as a class while passing in the necessary arguments
    process_creator = Marble_Creator(pipe_creator_to_bagger_send, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    process_bagger = Bagger(pipe_bagger_from_creator_receive, pipe_bagger_to_assembler_send, settings[BAG_COUNT], settings[BAGGER_DELAY])
    process_assembler = Assembler(pipe_assembler_from_bagger_receive, pipe_assembler_to_wrapper, settings[ASSEMBLER_DELAY])
    process_wrapper = Wrapper(pipe_wrapper_from_assembler_receive, settings[WRAPPER_DELAY], total_gifts)

    print('Starting the processes')
    

    # Start each process
    process_creator.start()
    process_bagger.start()
    process_assembler.start()
    process_wrapper.start()


    print('Waiting for processes to finish')
    # Wait for each process to finish

    process_creator.join()
    process_bagger.join()
    process_assembler.join()
    process_wrapper.join()
    display_final_boxes(BOXES_FILENAME)

    # Print the number of gifts created
    print(f'Total gifts created: {total_gifts.value}')


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")