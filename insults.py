from random import choice, randint

words = []
with open("insults.txt") as insults:
    lines = insults.readlines()
    temp = []
    for line in lines:
        if line.startswith('-'):
            words.append(temp)
            temp = []
            continue
        temp.append(line[:-1].lower())
    words.append(temp)
#print(words)
words2 = []
with open("insults2.txt") as insults:
    for line in insults.readlines():
        words2.append(line[:-1])
#print(words2)

def genInsult():
    if randint(0,5) != 0:
        insult = "You "
        for section in words:
            insult += choice(section)
            insult += ' '
        insult = insult[:-1]
        insult += '!'
    else:
        insult = choice(words2)
    return insult
