class FilteredSequence(object):
    def __init__(self, seq):
        self.object = seq

    def __iter__(self):
        return iter(self.object)

    def __str__(self):
        string = ''
        for i in self.object:
            string += str(i) + " "
        return string[:-1]

    def filter(self, foo):
        def it():
            for i in xrange(len(self.object)):
                if foo(self.object[i]):
                    yield self.object[i]
        return FilteredSequence(it())


a = FilteredSequence([1, 2, 3, 4, 5])
print a
print a.filter(lambda x: x % 2 == 0)
