class Defaultdict(dict):
    def __missing__(self, key):
        self[key] = Defaultdict()
        return self[key]


d = Defaultdict()
d['a']['b'] = 1

print d
