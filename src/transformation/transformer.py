import transformation.nounInversion as ni



def transformSentence(data, verbActive):
 
    verb = verbActive
    agent = data.get('agent')
    subjpass = ni.inversion(data.get('subjpass'))

    if agent != 'one':
          agent = ni.inversion(agent)

    
    subject = agent
    object =subjpass
    

    # Basic conversion (not considering verb tense adjustments)
   
    active_sentence = f"{subject} {verb} {object}".capitalize() + "."
    print(f"Active Sentence: {active_sentence}")
    
    return active_sentence
