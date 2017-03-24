def fib(n):
    a = 1
    b = 1
    print a, "\n", b
    if n > 2 :
        for i in range(n-2):
            c = b
            b += a
            a = c
            yield b

def main():
    n = 10
    for i in fib(n):
        print i

if __name__ == "__main__":
    main()
    



