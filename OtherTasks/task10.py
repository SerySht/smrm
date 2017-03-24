class Meta(type):
    def __new__(cls, name, bases, attrs):
        filename = attrs['filename']
        with open(filename, 'r') as file:
            for line in file:
                if line != "":
                    param = line.strip().split(' ')
                    key = param[0]
                    param.pop(0)
                    val = ''
                    for i in param:
                        val += i
                    attrs[key] = val

        return super(Meta, cls).__new__(cls, name, bases, attrs)


class Film(object):
    filename = 'metaclass.txt'
    __metaclass__ = Meta

film = Film()
print "--Film info--"
print "Name -", Film.Name
print "Year:", film.Year
print "Genre:", film.Genre
print "Produce by", film.ProducedBy
print "Music by", film.MusicBy
