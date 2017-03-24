class Vector(object):
    def __init__(self, *numbers):
        self.numbers = numbers

    def __add__(self, other):
        new_list = [[i + j for i, j in zip(self.numbers, other.numbers)]] + \
                   list((self.numbers[len(other.numbers):]
                         if len(self.numbers) > len(other.numbers)
                         else other.numbers[len(self.numbers):]))
        return new_list

    def __sub__(self, other):
        new_list = [[i - j for i, j in zip(self.numbers, other.numbers)]] + \
                    list((self.numbers[len(other.numbers):]
                         if len(self.numbers) > len(other.numbers)
                         else other.numbers[len(self.numbers):]))
        return (new_list)

    def __mul__(self, other):
        if type(other) == int:
            new_list = [i * other for i in self.numbers]
            return new_list
        else:
            new_list = [i * j for i, j in zip(self.numbers, other.numbers)] +\
                       list((self.numbers[len(other.numbers):]
                             if len(self.numbers) > len(other.numbers)
                             else other.numbers[len(self.numbers):]))
            return sum(new_list)

    def __eq__(self, other):
        if self.numbers == other.numbers:
            return True
        else:
            return False

    def __len__(self):
        return len(self.numbers)

    def __getitem__(self, item):
        return self.numbers[item]

    def __str__(self):
        return '{}'.format(self.numbers)

vector1 = Vector(1, 2, 3)
vector2 = Vector(4, 5, 6, 7)
print(vector1 * vector2)
print vector1

