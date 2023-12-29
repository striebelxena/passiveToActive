import spacy

def checkForPassive(sentence):

    for token in sentence:
      print(token) 
      print(token.dep_)
      print(token.tag_)
      if token.dep_ in ('nsubjpass', 'csubjpass') :
         print(token) 
         for token in sentence:
                if token.dep_ == 'auxpass': 
                    return True
    return False