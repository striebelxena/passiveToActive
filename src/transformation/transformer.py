import transformation.nounInversion as ni



def transformSentence(data, finalVerb):
 
    verb = finalVerb['activeVerb']
    auxilary = finalVerb['auxilaryVerb']
    agent = data.get('agent')
    subjpass = ni.inversion(data.get('subjpass'))
    
    adverbBefore = data.get('adverb')['bef']
    adverbAfter= data.get('adverb')['aft']
    cltreeAtStart = data.get('cltreeAtStart')
    cltree = data.get('cltree')
    cltree = ' '.join(cltree)
    prepAtStart = data.get('prepAtStart')
    prep = data.get('prep')
    prep = ' '.join(prep)
    xcomp = data.get('xcomp')
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

    components = [prepAtStart, cltreeAtStart, subject, auxilary, adverbBefore, verb, part, object, verbAddition, adverbAfter, cltree, prep, xcomp]
    # Entfernen Sie alle leeren Strings aus der Liste
    filtered_components = [comp for comp in components if comp]

    # Verbinden Sie die Komponenten mit einem Leerzeichen
    active_sentence = " ".join(filtered_components) + "."
    active_sentence = active_sentence[0].upper() + active_sentence[1:]

    print(active_sentence)

    return active_sentence
