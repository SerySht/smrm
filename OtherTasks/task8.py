class MyLogger(object):
    log = ''

    def __getattribute__(self, name):
        obj = object.__getattribute__(self, name)

        def get_log(*args):
            result = obj(*args)
            MyLogger.log += 'Called {0} with args {1}. '\
                            'Result: {2}\n'.format(name, args, result)
            return result

        if callable(obj):
            return get_log

        return object.__getattribute__(self, name)

    def __str__(self):
        return MyLogger.log


class ToLog(MyLogger):
    def foo(self, *args):
        i = 1
        for arg in args:
            i = i * arg
        return i

a = ToLog()
print a.foo(5, 5)
print str(a)
