import re

def repository():    
    result_set = set()
    while True:
        line = raw_input()
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
        elif command == 'exit':
            return()
        elif command == "greb":
            copy_set = result_set.copy()
            for i in range(len(result_set)):
                print (re.findall(words[0],copy_set.pop()))
        elif command == "save":
            f = open('file.txt', 'w')
            copy_set = result_set.copy()
            for i in range(len(copy_set)):
                f.writelines(copy_set.pop()+' ')                
            f.close()
        elif command == "load":
            f = open('file.txt', 'r')
            line = f.readline() 
            result_set.update(line.split())
            f.close()
        else:
            print "Wrong command"


if __name__ == "__main__":
    repository()
