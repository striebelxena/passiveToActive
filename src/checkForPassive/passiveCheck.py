import spacy

def checkForPassive(sentence):

    for token in sentence:
      print(token) 
      print(token.dep_)
      if token.dep_ == 'nsubjpass':
         print(token) 
         for token in sentence:
                if token.dep_ == 'auxpass': 
                    return True
    return False