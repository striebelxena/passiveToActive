import transformation.nounInversion as ni



def transformSentence(data, finalVerb):
 
    verb = finalVerb['activeVerb']
    auxilary = finalVerb['auxilaryVerb']
    agent = data.get('agent')
    subjpass = ni.inversion(data.get('subjpass'))
    adverbStart = data.get('adverb')['start']
    adverbBefore = data.get('adverb')['bef']
    adverbAfter= data.get('adverb')['aft']
    cltreeAtStart = data.get('cltreeAtStart')
    cltree = data.get('cltree')
    cltree = ' '.join(cltree)
    prepAtStart = data.get('prepAtStart')
    prep = data.get('prep')
    prep = ' '.join(prep)
    xcomp = data.get('xcomp')
    cconj = data.get('cconj')
    ccomp = data.get('ccomp')
    conj = data.get('conj')
    part = data.get('part')
    verbAddition = data.get('verbAddition')
    

    if agent != 'one':
          agent = ni.inversion(agent)

    
    subject = agent
    object =subjpass
    

    # Basic conversion (not considering verb tense adjustmen7ts)
   
    #active_sentence = f"{subject} {adverbBefore} {verb} {object} {adverbAfter} {cltree} {prep} {xcomp}" + "."
    #active_sentence = active_sentence[0].upper() + active_sentence[1:]

    """newsent = ' '.join(list(filter(None, [agent,auxstr,adverb['bef'],verb,part,subjpass,adverb['aft'],advcl,prep,xcomp])))+punc
    if not rec:
            newsent = newsent[0].upper() + newsent[1:]
    newdoc += newsent + ' '"""

    #components = [prepAtStart, cltreeAtStart, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp]
    # Entfernen Sie alle leeren Strings aus der Liste

    components = [adverbStart, prepAtStart, cltreeAtStart, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp, cconj, ccomp, conj]
    components = [comp for comp in components if comp]
    
    def remove_duplicates_and_substrings():
     for i, comp in enumerate(components):
      if comp:
        for j, other in enumerate(components):
            if i != j and comp in other:
                components[i] = ''
                break

    remove_duplicates_and_substrings()
   
    print("components:")
    print(components)

    filtered_components = [comp for comp in components if comp]
    """sorted_components = sorted(filtered_components, key=lambda x: len(x) if x else 0, reverse=True)


    def remove_duplicates_and_substrings(components):
      for comp in filtered_components:
        if any(comp in f_comp for f_comp in filtered_components if comp != f_comp):
            filtered_components[comp.i] = ''
      

    remove_duplicates_and_substrings(sorted_components)"""
    final_components = filtered_components

    print("final components:")
    print(final_components)
    
    # Verbinden Sie die Komponenten mit einem Leerzeichen
    active_sentence = " ".join(final_components) + "."
    active_sentence = active_sentence[0].upper() + active_sentence[1:]

    print(active_sentence)

    return active_sentence
