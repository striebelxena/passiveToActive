import transformation.nounInversion as ni



def transformSentence(data, verbActive):
 
    verb = verbActive
    agent = data.get('agent')
    subjpass = ni.inversion(data.get('subjpass'))
    adverbBefore = data.get('adverb')['bef']
    adverbAfter= data.get('adverb')['aft']
    subtree = data.get('subtree')
    prep = data.get('prep')
    xcomp = data.get('xcomp')


    if agent != 'one':
          agent = ni.inversion(agent)

    
    subject = agent
    object =subjpass
    

    # Basic conversion (not considering verb tense adjustmen7ts)
   
    active_sentence = f"{subject} {adverbBefore}{verb}{object}{adverbAfter} {subtree} {prep} {xcomp} ".capitalize() + "."
    """newsent = ' '.join(list(filter(None, [agent,auxstr,adverb['bef'],verb,part,subjpass,adverb['aft'],advcl,prep,xcomp])))+punc
    if not rec:
            newsent = newsent[0].upper() + newsent[1:]
    newdoc += newsent + ' '"""
    

    return active_sentence
