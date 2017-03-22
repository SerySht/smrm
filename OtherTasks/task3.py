def repository(filename):
    f = open(filename, "r")
    result_set = set()
    for line in f:
        words = line.split()
        command = words[0]
        words = words[1:]

        if command == "add":
            result_set.update(words)
        elif command == "remove":
            for i in range(len(words)):
                result_set.discard(words[i])
        elif command == "find":
            for i in range(len(words)):
                if words[i] in result_set:
                    print words[i], '- exist'
                else:
                    print words[i], "- don't exist"
        elif command == "list":
            print result_set
        else:
            print "Wrong command"


if __name__ == "__main__":
    repository()
