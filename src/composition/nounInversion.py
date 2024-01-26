noundict = {'i':'me', 'we':'us', 'you':'you', 'he':'him', 'she':'her', 'they':'them', 'them':'they', 'her':'she', 'him':'he', 'us':'we', 'me':'i'}

def inversion(noun):
    n = noun.lower()
    if n in noundict:
        newNoun = noundict[n]
        if(newNoun== "i"):
            newNoun = newNoun.capitalize()
        return newNoun
    else:
        return noun
