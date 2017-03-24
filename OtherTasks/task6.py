class Error(TypeError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def to_json(obj, raise_unknown=False):
    if isinstance(obj, str):
        return '\"%s\"' % obj

    elif (isinstance(obj, int) or isinstance(obj, long) or
          isinstance(obj, float)):
        return '%g' % obj

    elif isinstance(obj, bool):
        return str(obj).lower()

    elif type(obj) is None:
        return 'null'

    elif isinstance(obj, tuple) or isinstance(obj, list):
        return '[' + ', '.join(to_json(x, raise_unknown) for x in obj) + ']'

    elif isinstance(obj, dict):
        result = '{'
        count = len(obj)
        for key in obj.keys():
            count -= 1
            if not (isinstance(key, str) or isinstance(key, int) or
                    isinstance(key, long) or isinstance(key, float)):
                raise TypeError('Key must be string type!')
            result += (to_json(str(key), raise_unknown) + ': ' +
                       to_json(obj[key], raise_unknown))
            if count > 0:
                result += ', '
            else:
                result += '}'
        return result

    elif raise_unknown:
        raise Error("Don't know such a type:" + str(type(obj)))


def foo():
    pass

print to_json("kek")
print to_json(1234)
try:
    to_json(foo, raise_unknown = True)
except Error as err:
    print err

