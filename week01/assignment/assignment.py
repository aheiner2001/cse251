'''
Time Guesstimate to complete:
Proficient with all the "Know how to" statements:                       1 hour
Familiar with the "Know how to" statements, but need to review a few:   1 - 4 hours
Need to review most the "Know how to" statements:                       4 - 8 hours
Need to review/relearn all the "Know how to" statements:                8+ hours

All ASSERTS must pass. Everything in this assignment should have been learned
previously. If there are holes in your knowledge, then this is the time to 
fill them (meaning learn the concepts). Take the time to learn by reading
the provided links. There are no group "prove" assignments in this class.

Make sure to write comments above your functions, explaining in your own
words what the functions does. Your comments are your "digital signature",
showing that you both wrote the code and understand how it works.

Grading:
Not passing an assert or answering #10 and #12: 0 points (code must pass all asserts--this is only true of this first assignment)
'''

from unittest import TestCase
from cse251functions import *

# 1)
# Defines the function perform_math with 3 parameters
# type hints are used to help specify which values are being used
def perform_math(intial_value: int, value: int, operation: str) -> float:

    # The first if statement will check is the given operation is equal to the addition operation
    # if so, the sum of the two value are returned
    if operation == "+":
        return intial_value + value;
        

    # else if  statement will check is the given operation is equal to the subtraction operation
    # if so, the difference of the two value are returned
    elif operation == "-":
        return intial_value - value
    

     # else if statement will check is the given operation is equal to the multiplication operation
    # if so, the pruduct of the two value are returned         
    elif operation == "*":
            return intial_value * value
    
    # else if statement will check is the given operation is equal to the division operation
    # if so, the quotient of the two value are returned         
    elif operation == "/":
         return intial_value / value
    
        # else if statement will check is the given operation is equal to the floor division operation
    # if so, the floor of  qquiotenthe two value are returned      
    elif operation == "//":
         return intial_value // value
    
   # else if statement will check is the given operation is equal to **
    # if so, the first number will we raised to the power of the second value
    elif operation == "**":
         return intial_value ** value
    
# if operation does not exist then raise an error
    else:
         raise ValueError(f"Operation does not exist: {operation}")

 
# 2) 
# funciton is defines as determined 
# the return statement finds the index of the given word
def find_word_index(word_to_find: str , words: list)-> int:
     return words.index(word_to_find)
          

# 3 funtion to return the str located with the key of a dict
def get_value_from_dict_using_key( key: str, word_dict: dict)-> str:
     return word_dict[key]
     

# 4)  returns a url with the provided key
def get_list_of_urls_from_dict(key: str, url_dict: dict) -> list:
     return url_dict[key]

# 
def find_url(urls: list, name: str) -> str:
     
    # list is defined
     list_of_urls= []

    #  search each url in the list
     for url in urls:
        #   if statement to check to see if name is in the Url, if so it will add it to the list and then return that list
          if name in url:
               list_of_urls.append(url)
    
     return list_of_urls

# 6) Opens a file.

# for each line in the file we will check if the string in that that line, if it ever occurs we will then return true
def find_str_in_file(filename: str, str_to_find: str) -> bool:
    with open(filename, "r") as file:  
        for line in file:
            if str_to_find in line:
                return True
    return False
          




# parent class definition: there are three variables.

class MyParentClass:

    def __init__(self, value: int, values: list, name:str):
        self.value = value
        self.values = values
        self.name = name
         
        #  when called on an object it will return the value at the specified index
    def get_value_using_index(self, value):
         return self.values[value]        
         
         
     

# 8
# definition of MyChildClass
class MyChildClass(MyParentClass):
     def __init__(self, value: int, values: list, name:str, age:int ):
        # we use the super construcotr to pass in values from the parent

        super().__init__(value, values, name )

# we add the age to the child 
        self.age = age
      

# 9) 
# we are simply appending to the list to demonstate the mutability, return the index of 0
def pass_by_reference_mutable_example(lists_are_passed_by_reference_and_mutable: list, str_to_add: str)-> str:
     lists_are_passed_by_reference_and_mutable.append(str_to_add)
     return lists_are_passed_by_reference_and_mutable[0]
     
#      10) TODO: Provide a quick explanation of what pass-by-reference means. Also, what does mutable mean?
# mutable means that it is changeable

#
# we do not change the original value of the list since we are only using a refenece of it and then returning the result
def pass_by_reference_immutable_example( strings_are_pass_by_reference_and_immutable: str,str_to_add: str )->str:
     result = strings_are_pass_by_reference_and_immutable + str_to_add
     return result
#      12) TODO: What does immutable mean?
# Immutable means that is cannot be change, 

# Don't change any of the assert lines. All asserts should pass. You should see "All tests passed!" if all assert pass.
# If an assert doesn't pass, you will see an AssertionError (see https://www.w3schools.com/python/ref_keyword_assert.asp).
# The AssertionError will show you why it didn't pass (meaning, it is not an error with the assertion code, but with your code)

def main():
    ''' Know how to:
        - Call a function
        - Pass in parameters to a function in the correct order
        - Use correct parameter data types
        - Return a value from a function
        - Return correct data type from a function
        - Return from all call paths in a a function
        - Write an IF statement
        - Reading: https://www.geeksforgeeks.org/python-functions/
    '''
    assert perform_math(10, 1, "+") == 11
    assert perform_math(1, 10, "+") == 11
    assert perform_math(10, 1, "-") == 9
    assert perform_math(1, 10, "-") == -9
    assert perform_math(10, 2, "*") == 20
    assert perform_math(2, 10, "*") == 20
    assert perform_math(10, 2, "/") == 5
    assert perform_math(2, 10, "/") == 0.2
    assert perform_math(10, 3, "//") == 3
    assert perform_math(3, 10, "//") == 0
    assert perform_math(10, 3, "**") == 1000
    assert perform_math(3, 10, "**") == 59049

    ''' Know how to:
        - Use a list
        - Use the index function on a list
        - Reading: https://www.geeksforgeeks.org/python-lists/
    '''
    assert find_word_index("a", ["a", "b", "c", "h"]) == 0
    assert find_word_index("b", ["a", "b", "c", "h"]) == 1
    assert find_word_index("c", ["a", "b", "c", "h"]) == 2
    assert find_word_index("h", ["a", "b", "c", "h"]) == 3

    ''' Know how to:
        - Use a dictionary
        - Use a key to get the value in a dictionary
        - Understand that a dictionary value can be list
        - Know how to get the list using a key
        - Know how to write a FOR loop
        - Know how to use "in" keyword
        - Reading: https://www.geeksforgeeks.org/python-dictionary/
    '''
    word_dict = {"k1": 1, "k2": 2, "k3": 3, "k4": 10}
    assert get_value_from_dict_using_key("k1", word_dict) == 1
    assert get_value_from_dict_using_key("k2", word_dict) == 2
    assert get_value_from_dict_using_key("k3", word_dict) == 3
    assert get_value_from_dict_using_key("k4", word_dict) == 10


    movie_dict = {"people": ["http://127.0.0.1:8790/1", "http://127.0.0.1:8790/2", "http://127.0.0.1:8790/3"], "films":
                  ["http://127.0.0.1:8790/film1", "http://127.0.0.1:8790/film2", "http://127.0.0.1:8790/film3"]}
    urls = get_list_of_urls_from_dict("films", movie_dict)
    url = find_url(urls, "film3")
    assert url != None

    '''
        - Know how to make a Python Class
        - Know how to write a constructor
        - Know how to make attributes in a constructor
        - Understand how to use "self" in Python
        - Know how to instantiate an object of a class (shown below)
        - Know how to obtain the value using the object's attribute (shown below)
        - Know what a method is and how to write one
        - Know how to return a value from a method
        - Know to obtain a value at a specific index in a list
        - Know how to extend a class
        - Understand that an extended/child class inherits everything from parent class
        - Readings: https://www.geeksforgeeks.org/python-classes-and-objects/, https://www.geeksforgeeks.org/extend-class-method-in-python/, https://realpython.com/python-super/
    '''
    # 13) TODO instantiate an object using MyParentClass with the following three parameters: (1, [5, 6, 7], "3")
    obj = MyParentClass(1, [5, 6, 7], "3")
    assert obj.value == 1
    assert obj.values == [5, 6, 7]
    assert obj.name == "3"
    assert obj.get_value_using_index(0) == 5
    assert obj.get_value_using_index(1) == 6
    assert obj.get_value_using_index(2) == 7

    # 14) TODO instantiate an object using MyChildClass with the following four parameters: (1, [5, 6, 7], "3", 10).
    # 15) TODO: do NOT duplicate the code in the parent class when writing the child class. For example, the parent
    # class constructor already creates the value, values, and name parameters. Do not write these in the child
    # class. Instead, the child constructor should call the parent constructor. Same for the 'get_value_using_index'
    # function, do not rewrite this in the child class.
    childObj = MyChildClass(1, [5, 6, 7], "3", 10)
    assert childObj.value == 1
    assert childObj.values == [5, 6, 7]
    assert childObj.name == "3"
    assert childObj.age == 10
    assert childObj.get_value_using_index(0) == 5
    assert childObj.get_value_using_index(1) == 6
    assert childObj.get_value_using_index(2) == 7
    assert isinstance(childObj, MyParentClass) == True

    '''
        - Know how to open a file
        - Know how to read lines from a file
        - Understand how to compare strings
        - Readings: https://www.geeksforgeeks.org/open-a-file-in-python/, https://www.geeksforgeeks.org/with-statement-in-python/
    '''
    assert find_str_in_file("data.txt", "g") == True
    assert find_str_in_file("data.txt", "1") == False

    '''
        - Know the difference between pass-by-reference and pass-by-value.
        - Reading: https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference (read the first answer)
        - Technically python is pass-by-object-reference, if you are intested in the difference, read https://www.geeksforgeeks.org/pass-by-reference-vs-value-in-python/
    '''
    l = ["abc", "def", "ghi"]
    pass_by_reference_mutable_example(l, "jkl")
    assert len(l) == 4
    assert l[3] == "jkl"
    s = "strings are immutable"
    new_string = pass_by_reference_immutable_example(
        s, " so adding to it creates a new object in memory")
    assert id(s) != id(new_string)
    assert len(new_string) != len(s)

    print("All tests passed!")


if __name__ == '__main__':
    main()
    create_signature_file("CSE251W25")
 