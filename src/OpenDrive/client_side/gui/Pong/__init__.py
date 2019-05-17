

class Person(object):

    anzahl_personen = 0

    def __init__(self, name: str, alter: int, haarfarbe: str = "Blond"):
        self.name = name
        self.alter = alter
        self.haarfarbe = haarfarbe
        Person.anzahl_personen += 1

    def getName(self) -> str:
        return self.name

    def geburtstag(self) -> None:
        self.alter += 1

    @staticmethod
    def getAnzahlPersonen():
        return Person.anzahl_personen

    def __repr__(self):
        return f"Person(name={self.name})"


p1 = Person(name="John", alter=45, haarfarbe="Rot")
print(p1.haarfarbe)
print(str(p1))


class Number:

    def __init__(self, value):
        self.value = value

    def __add__(self, other: 'Number'):
        if isinstance(other, int):
            return Number(self.value + other)
        return Number(self.value + other.value)


n1 = Number(10)
n2 = Number(20)
n3 = n1 + 10

print(n3.value)