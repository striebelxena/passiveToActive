import spacy
import pattern.text.en as en

nlp = spacy.load("en_core_web_lg")


def analyseSentence(sentence):

    # Init parts of sentence to capture:
    subjpass = ''
    subj = ''
    verb = ''
    verbTense = ''
    verbPerson = '1'
    verbMood = ''
    verbAspect = ''
    adverb = {'bef':'', 'aft':''}
    part = ''
    prepAtStart = ''
    prep = list()
    agent = ''
    agentExists = False
    aplural = False
    aNumber = en.SINGULAR
    cltreeAtStart = ''
    cltree = list()
    aux = list(list(nlp('. .').sents)[0]) # start with 2 'null' elements
    xcomp = ''
    punc = '.'
    
    print("cltree")
    print(cltree)


    for word in sentence:
        print(f"Text: {word.text}")
        print(f"Part of Speech: {word.pos_}") # POS Tagging
        print(f"Lemma: {word.lemma_}") # Lemmatization
        print(f"Dependency relation: {word.dep_}")  # Dependency Parsing
        print(f"explain: {spacy.explain(word.dep_)}")
        print(f"Detailed POS tag: {word.tag_}")
        print(f"explain: {spacy.explain(word.tag_)}")
        print(f"morph: {word.morph}")
        print(f"morph Tense: {word.morph.get('Tense')}")
        print(f"morph Number: {word.morph.get('Number')}")
        print(f"morph Person: {word.morph.get('Person')}")
        print(f"morph Mood: {word.morph.get('Mood')}")
        print(f"morph VerbForm: {word.morph.get('VerbForm')}")
        print(f"morph Voice: {word.morph.get('Voice')}")
        print(f"morph Aspect: {word.morph.get('Aspect')}")
        print(f"morph Case: {word.morph.get('Case')}")        
        print(f"Head: {word.head}")
        print(f"Head dep: {word.head.dep_}")
        print(word.subtree)
        print("Subtree:")
        for subtree in word.subtree:
            print(subtree)
        print("\n")


        if word.dep_ in ('acl','advcl', 'relcl'):
            print("acl found")
            print(word.text)
            print(cltree)
            if word.head.dep_ in ('ROOT', 'auxpass'):
                  for c in  word.children :
                    if c.is_sent_start:
                        cltreeAtStart = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                        found_sent_start = True
                        break
                  if not found_sent_start:
                    cltree_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    cltree += [cltree_str]
        if word.dep_ == 'nsubjpass':
                 if word.head.dep_ == 'ROOT':
                    subtree_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    subjpass = subjpass + subtree_str
        if word.dep_ == 'nsubj': 
            subj = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
            #if word.head.dep_ == 'auxpass': 
            """if word.head.head.dep_ == 'ROOT': 
                    subjpass = subj """
        if word.dep_ in ('advmod','npadvmod','oprd', 'amod'):
            if word.head.dep_ == 'ROOT':
                if verb == '':
                    adverb['bef'] = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                else:
                    adverb['aft'] = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
        if word.dep_ == 'auxpass': 
            verbForm = word.morph.get('VerbForm')
            if sentence[word.i-1].lemma_ == 'have':    
                        verbAspect = en.PARTICIPLE
                        verbTense = en.PAST
                        verbForm = en.PARTICIPLE
            if sentence[word.i-1].lemma_ == 'will':    
                        verbTense = en.PRESENT
            elif word.tag_ == 'VBZ': #3rd person singular
                verbPerson = en.THIRD
                verbTense = en.PRESENT
            elif word.tag_ == 'VB':
                    verbTense = en.PRESENT #if auxpass is infinitive, the active verb should be present
            elif word.tag_ == 'VBD':
                        verbTense = en.PAST
            elif word.tag_ == 'VBG':
                        verbTense = en.PRESENT
                        verbAspect = en.PROGRESSIVE
            elif word.tag_ == 'VBN':
                        verbTense = en.PAST
            elif word.tag_ == 'VBP' or word.tag_ == 'VBZ':
                verbTense = en.PRESENT
            elif word.tag_ == 'MD':
                verbTense = en.PRESENT
            else:
                verbTense = en.tenses(word.text)[0][0]
            """if 'Inf' in verbForm:
                print("Infinitive found")
                verbTense = en.PRESENT
            else:
                verbTense = word.morph.get('Tense')
            if word.head.dep_ in ('ROOT', 'advcl'): 
                if not subjpass: # if no nsubjpass is found:
                    subjpass = subj"""

        if word.dep_ in ('aux','auxpass','neg'):
            if word.head.dep_ == 'ROOT':
                aux += [word]
        if word.dep_ == 'ROOT':
            verb = word.text
            verbLemma = word.lemma_
            if sentence[word.i+1].tag_ == 'IN':
                 verbAddition = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in sentence[word.i+1].subtree).strip()
        if word.dep_ == 'prt':
            if word.head.dep_ == 'ROOT':
                part = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
        if word.dep_ == 'prep':
            if word.head.dep_ == 'ROOT':
                  if word.is_sent_start:
                    prepAtStart = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                  else:
                    prep_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    prep += [prep_str]
        if word.dep_.endswith('obj'):
            if word.head.dep_ == 'agent':
                if word.head.head.dep_ == 'ROOT':
                    agent = ''.join(w.text + ', ' if w.dep_=='appos' else (w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws) for w in word.subtree).strip()
                    aplural = word.tag_ in ('NNS','NNPS')
        if word.dep_ == "agent":
            agentExists = True
        if word.dep_ in ('xcomp','ccomp','conj'):
            if word.head.dep_ == 'ROOT':
                print("recursion should be triggered")
                xcomp = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                """Sthat = xcomp.startswith('that')
                xcomp = pass2act(xcomp, True).strip(' .')
                if not xcomp.startswith('that') and that:
                    xcomp = 'that '+xcomp
        if word.dep_ == 'punct' and not rec:
            if word.text != '"':
                punc = word.text"""
    if not agentExists: # if no agent is found:
        agent = "one"
        aplural = False
    
    if aplural:
        aNumber = en.PLURAL

    print(f"subjpass: {subjpass}")
    print(f"subj: {subj}")
    print(f"verb: {verb}")
    print(f"verbForm: {verbForm}")
    print(f"verbTense: {verbTense}")
    print(f"verbPerson: {verbPerson}")
    print(f"verbMood: {verbMood}")
    print(f"adverb: {adverb}")
    print(f"part: {part}")
    print(f"prep: {prep}")
    print(f"agent: {agent}")

    print(f"aplural: {aplural}")

    print(f"cltree: {cltree}")
    print(f"aux: {aux}")
    print(f"xcomp: {xcomp}")
    print(f"punc: {punc}")
    print("\n")



    results = {
        "subjpass": subjpass,
        "subj": subj,
        "verb": verb,
        "verbLemma": verbLemma,
        "verbForm": verbForm,
        "verbTense": verbTense,
        "verbPerson": verbPerson,
        "verbAspect": verbAspect,
        "verbMood": verbMood,
        "adverb": adverb,
        "part": part,
        "prepAtStart": prepAtStart, # prepAtStart ist ein String, der das Präpositionalobjekt am Satzanfang enthält
        "prep": prep,
        "agent": agent,
        "aplural": aplural,
        "aNumber": aNumber,
        "cltreeAtStart": cltreeAtStart, # cltreeAtStart ist ein String, der das Präpositionalobjekt am Satzanfang enthält
        "cltree":  cltree,  # Konvertieren Sie subtree in eine Liste von Strings, falls nicht None
        "aux": [a.text for a in aux],  # Konvertieren Sie aux in eine Liste von Texten der Wörter
        "verbAddition": verbAddition,
        "xcomp": xcomp,
        "punc": punc
        }

    return results

