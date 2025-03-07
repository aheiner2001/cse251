'''
Requirements:
1. Create a class that extends the 'threading.Thread' class (see https://stackoverflow.com/questions/15526858/how-to-extend-a-class-in-python). This means that the class IS a thread. 
   Any objects instantiated using this class ARE threads.
2. Instantiate this thread class that computes the product of all numbers 
   between one and that number (exclusive)
3. COMMENT every line that you write yourself.

Things to consider:
a. How do you instantiate a class and pass in arguments (see https://realpython.com/lessons/instantiating-classes/)?
b. How do you start a thread object (see this week's reading)?
c. How will you wait until the thread is done (see this week's reading)?
d. How do you get the value an object's attribute (see https://datagy.io/python-print-objects-attributes/)?
'''

import threading
from cse251functions import *

###############################
# DO NOT USE YOUR OWN GLOBALS #
###############################
# here is my very owen thread class, which is a subclass of the threading.Thread class
# takes the number n as an argument
# the run method finds the product of all numbers between 1 and n
class myVeryOwnThread(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.n = n
        self.product = 1

    def run(self):
        for i in range(1, self.n):
         self.product *= i
    


def main():


    # first instance of my thread class
    firstThread = myVeryOwnThread(5)

    # we start the first Thread
    firstThread.start()

    # we wait for the first thread to finish
    firstThread.join()
    
    assert firstThread.product == 24, f'The product should equal 24 but instead was {
        firstThread.product}'

    # Repeat, passing in 10 (delete this line).
    secondThread = myVeryOwnThread(10)
    secondThread.start()
    secondThread.join()
    # Repeat, passing in 10 (delete this line).
    assert secondThread.product == 362880, f'The product should equal 362880 but instead was {
        secondThread.product}'
    
    # we do this one more time wth 15
    thirdThread = myVeryOwnThread(15)
    thirdThread.start()
    thirdThread.join()

    # Repeat, passing in 15 (delete this line).
    assert thirdThread.product == 87178291200, f'The product should equal 87178291200 but instead was {
        thirdThread.product}'


if __name__ == '__main__':
    main()
    print("DONE")
    create_signature_file("CSE251W25")
