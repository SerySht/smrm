import re


def text_statistics(filename):
    f = open(filename, "r")
    text = f.readline()
    print text
    number_of_words_in_sentence = []

    number_of_sentences = text.count('.')
    if number_of_sentences == 0:
        number_of_sentences = 1

    words = re.findall(r"\w+", text)
    number_of_words = len(words)
    dict_of_words = dict()

    for word in words:
        if dict_of_words.get(word) is None:
            dict_of_words[word] = 1
        else:
            dict_of_words[word] += 1

    print "---How many times each word is repeated in this text---"
    for i in dict_of_words.keys():
        print i, '-', dict_of_words[i]

    print "\nThe average number of words in the sentence:", number_of_words/number_of_sentences

    print "\nThe medium number of words in the sentence:",
    sentences = text.split('.')
    for i in range(len(sentences) - 1):
        number_of_words_in_sentence.append(len(sentences[i].split()))
    number_of_words_in_sentence.sort()
    print number_of_words_in_sentence[len(number_of_words_in_sentence)/2 + 1]

    print "\ntop-k n-gram:"
    n = 4
    k = 10
    top = {}
    for i in range(len(words)):
        word = str(words[i])
        for j in range(len(word)):
            gram = ""
            for m in range(min(n, len(word))):
                if(j + m) > len(word)-1 or len(word)-j < n:                #WTF!!!!!
                    break
                gram += word[j + m]
            if gram == "":
                continue
            if top.get(gram) is None:
                top[gram] = 1
            else:
                top[gram] += 1

    print sorted(top.items(), key=lambda x: x[1], reverse=True)
    f.close()

if __name__ == '__main__':
    text_statistics()
