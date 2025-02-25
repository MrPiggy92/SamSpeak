from random import choice

words = []
with open("insults.txt") as insults:
    lines = insults.readlines()
    temp = []
    for line in lines:
        if line.startswith('-'):
            words.append(temp)
            temp = []
            continue
        temp.append(line[:-1])
    words.append(temp)
#print(words)

def genInsult():
    insult = "You "
    for section in words:
        insult += choice(section)
        insult += ' '
    insult = insult[:-1]
    insult += '!'
    return insult
