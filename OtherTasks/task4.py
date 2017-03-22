def fib(filename):
    f = open(filename, "r")
    text = f.readline()
    a = 1
    b = 1
    print a, "\n", b
    for i in range(10):
        c = b
        b += a
        a = c
        print b

if __name__ == "__main__":
    fib()



