class Person:

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def getNm(self):
        return f"returning anme form getName methos: {self.name}"

    def __str__(self):
        return(f"{self.name} has a grade of {self.grade}")
