import pickle
from MyClass import Person

person1 = Person("Brandon", 100)
person2 = Person("remy", 100)
person3 = Person("shemy", 100)

with open("grade.dat", "wb") as f: 
    b = pickle.dumps(person1)
    f.write(b)