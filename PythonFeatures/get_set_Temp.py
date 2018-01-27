class Person:
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if 150 > age > 0:
            self._age = age

    def __init__(self, name, age):
        self._name = name
        self._age = age


p = Person('xiaohong', 30)
p.age = 30
print(p.age)