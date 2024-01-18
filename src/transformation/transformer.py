import transformation.nounInversion as ni



def transformSentence(data, finalVerb, preClause, postClause):
 
    verb = finalVerb['activeVerb'].strip()
    auxilary = finalVerb['auxilaryVerb'].strip()
    agent = data.get('agent')
    subjpass = ni.inversion(data.get('subjpass'))
    adverbStart = data.get('adverb')['start']
    adverbBefore = data.get('adverb')['bef']
    adverbAfter= data.get('adverb')['aft']
    cltreeAtStart = data.get('cltreeAtStart')
    print("cltreeatStart")
    print(cltreeAtStart)
    print(len(cltreeAtStart))
    cltree = data.get('cltree')
    print("cltree")
    print(cltree)
    print(len(cltree))
    #if len(cltree) > 1:
    cltree = ' '.join(cltree)
    #cltree = str(cltree)
    prepAtStart = data.get('prepAtStart')
    #prepAtStart = ' '.join(prepAtStart)
    prep = data.get('prep')
    prep = ' '.join(prep)
    xcomp = data.get('xcomp')
    cconj = data.get('cconj')
    ccomp = data.get('ccomp')
    conj = data.get('conj')
    part = data.get('part')
    verbAddition = data.get('verbAddition')
    wsubj = data.get('wsubjpass')
    mark = data.get('mark')
    mark = ' '.join(mark)
    #mark = str(mark)
    punc = data.get('punc')
    preClause = str(preClause)
    postClause = str(postClause)    
    finalClause = ""

    if agent != 'one':
          agent = ni.inversion(agent)

    
    subject = agent
    
    object = subjpass
    

    # Basic conversion (not considering verb tense adjustmen7ts)
   
    #activeClause = f"{subject} {adverbBefore} {verb} {object} {adverbAfter} {cltree} {prep} {xcomp}" + "."
    #activeClause = activeClause[0].upper() + activeClause[1:]

    """newsent = ' '.join(list(filter(None, [agent,auxstr,adverb['bef'],verb,part,subjpass,adverb['aft'],advcl,prep,xcomp])))+punc
    if not rec:
            newsent = newsent[0].upper() + newsent[1:]
    newdoc += newsent + ' '"""

    #components = [prepAtStart, cltreeAtStart, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp]
    # Entfernen Sie alle leeren Strings aus der Liste

    

    #components = [mark, adverbStart, prepAtStart, cltreeAtStart, wsubj, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp, cconj, ccomp, conj]
    

    
    components = [mark, adverbStart, prepAtStart, cltreeAtStart, wsubj, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp, ccomp, conj]
    print("initial components:")
    print(components)
    components = [comp for comp in components if comp]
    def remove_duplicates_and_substrings():
     for i, comp in enumerate(components):
      if comp:
        for j, other in enumerate(components):
            if i != j and comp in other:
                components[i] = ''
                break

    #remove_duplicates_and_substrings()
   
    print("unique components:")
    print(components)

    filtered_components = [comp for comp in components if comp]
    """sorted_components = sorted(filtered_components, key=lambda x: len(x) if x else 0, reverse=True)


    def remove_duplicates_and_substrings(components):
      for comp in filtered_components:
        if any(comp in f_comp for f_comp in filtered_components if comp != f_comp):
            filtered_components[comp.i] = ''
      

    remove_duplicates_and_substrings(sorted_components)"""


    final_components = filtered_components

    # if last elements ends with a punctuation mark or whitespace, remove it
    if final_components[-1][-1] in ('.', '?', '!', ',', ':', ';', ' '):
       ("final components schleife")
       final_components[-1] = final_components[-1][:-1]

    
    
    if postClause.endswith('.'):
       postClause = postClause[:-1]
    
    
    print(final_components[-1][-1])

    print("final components:")
    print(final_components)

    print("preClause")
    print(preClause)
    print("postClause")
    print(postClause)
    
    finalClause =  " ".join(final_components).split()
    print("final clause length")
    #finalClause = nlp(finalClause)
    newLength = len(finalClause)
    print(newLength)
    #finalClause = str(finalClause)
    # Zerlege die Wörter und Satzzeichen in final_components
    # words_and_punctuation_list = " ".join(final_components).split()

    # Berechne die Anzahl der Wörter
    """ word_count = sum(1 for token in finalClause if token.isalpha())

    # Berechne die Anzahl der Satzzeichen
    punctuation_count = len(finalClause) - word_count
    print("Anzahl der Satzzeichen in final_components:", punctuation_count)
    print("Anzahl der Wörter in final_components:", word_count)

    newLength = len(finalClause.split()) + punctuation_count

   

    #newLength = len(finalClause.split()) 
    """
    finalClause = ' '.join(finalClause)

    if preClause and preClause != 'false':
      finalClause = preClause + " " + finalClause
    if postClause and postClause != 'false':
      if postClause == '.':
        finalClause = finalClause  
      elif postClause.startswith(","):
          finalClause = finalClause + postClause
      else:
          finalClause = finalClause + " " + postClause
         
    
    finalClause = finalClause[0].upper() + finalClause[1:]
   
    print(finalClause)

    return finalClause, newLength
