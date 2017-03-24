cache_dict = {}

def cached(foo):
    def wrapper_func(*args):
        print cache_dict
        if foo in cache_dict:
            if str(args) in cache_dict[foo]:
                print "Taking existing result:"
                return cache_dict[foo][str(args)]

        print "Making new result:"
        res = foo(*args)
        cache_dict[foo] = {str(args): res}
        return res
 
    return wrapper_func
 
 
@cached
def add(*args):
    return args[0] + args[1]

@cached
def sub(*args):
    return args[0] - args[1]

print add(5, 5)
print add(5, 5)
print add(5, 6)
print sub(5, 3)
print sub(5, 5)

