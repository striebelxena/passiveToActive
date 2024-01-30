noundict = {
    "i": "me",
    "we": "us",
    "you": "you",
    "he": "him",
    "she": "her",
    "they": "them",
    "them": "they",
    "her": "she",
    "him": "he",
    "us": "we",
    "me": "i",
}


def inversion(noun):
    """
    Input: a noun
    This function checks if the noun is in the dictionary and returns the inverted pronoun
    Output: the inverted pronoun
    """
    n = noun.lower()
    if n in noundict:
        newNoun = noundict[n]
        if newNoun == "i":
            newNoun = newNoun.capitalize()
        return newNoun
    else:
        return noun
