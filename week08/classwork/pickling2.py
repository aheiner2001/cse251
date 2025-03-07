import pickle

with open ("grade.dat", "rb") as f:
    person1 = pickle.load(f)

    print(f"person1: {person1}")
    print(f"person1: {person1.getNm()}")