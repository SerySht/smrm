class MyXrange(object):
    def __init__(self, *args):
        if len(args) == 1:
            self.start = 0
            self.end = args[0]
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.end = args[1]
            self.step = 1
        elif len(args) == 3:
            self.start = args[0]
            self.end = args[1]
            if args[2] == 0:
                raise ValueError("Step cannot be equal zero")
            self.step = args[2]

    def __len__(self):
        return (self.end - self.start) // self.step

    def __getitem__(self, item):
        if item > len(self):
            raise IndexError()
        return self.start + item * self.step

    def __iter__(self):
        self.i = 0
        while self.i < len(self):
            yield self.__getitem__(self.i)
            self.i += 1


for i in MyXrange(20, 1, -1):
    print i
