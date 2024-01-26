import spacy
import pattern.text.en as en

nlp = spacy.load("en_core_web_lg")
from spacy.tokens import Token



def analyseSentence(sentence, source):

    # Init parts of sentence to capture:
    subjpass = ''
    subj = ''
    verb = ''
    verbTense = ''
    verbPerson = '1'
    verbMood = ''
    verbAspect = ''
    verbAddition = ''
    verbForm = ''
    adverb = {'start':'','bef':'', 'aft':''}
    part = ''
    prepAtStart = ''
    prep = list()
    mark = list()
    agent = ''
    agentExists = False
    aplural = False
    aNumber = en.SINGULAR
    cltreeAtStart = ''
    cltree = list()
    aux = list(list(nlp('. .').sents)[0]) # start with 2 'null' elements
    cconj = ''
    xcomp = ''
    conj = ''
    ccomp = ''
    punc = ''
    wsubjpass = ''
    found_sent_start = False
    subclause = ''
    structure = {}
    passiveSentences = list()
    usedIndex = []
    
    print("cltree")
    print(cltree)


  

    # Add custom extension to Token class to save the position of the token in the sentence
    if not Token.has_extension("sentPosition"):
        Token.set_extension("sentPosition", default= 1)

        for token in sentence:
            token._.sentPosition = token.i

        for token in sentence:
            print(f"token: {token.text}, sentPosition: {token._.sentPosition}")

    # General analysis of sentence structure 

    for word in sentence:
         if word.dep_ in ('acl','advcl', 'relcl', 'ccomp', 'xcomp', 'csubj', 'cobj', 'conj', 'cc', 'auxpass', 'subjpass', 'nsubjpass', 'dobj', 'iobj', 'agent', 'pcomp', 'acomp', 'appos', ):
                subclause = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                structure[f"{word.dep_} {word._.sentPosition} " ] = subclause
                sub_clause = nlp(subclause)
                has_auxpass = any(word.dep_ == "auxpass" for word in sub_clause)
                has_nsubjpass = any(word.dep_ == "nsubjpass" for word in sub_clause)

                if has_auxpass and has_nsubjpass:
                    passiveSentences.append(subclause)  

    print("passiveSentences")
    print(passiveSentences) 
    
    print("structure")
    print(structure)
    #pattern = structur

    print("chunks")
            
    for chunk in sentence.noun_chunks:
        print(chunk.text)

    for word in sentence:
     if word.i not in usedIndex:
        if source != 'fileTransformation':
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
            print("acl")
            print(word)
            if word.head.dep_ in ('ROOT', 'auxpass'):
                cltree_span = list(word.subtree)
                for span_word in cltree_span:
                    if span_word.i not in usedIndex:
                        usedIndex.append(span_word.i)

                print("cltree_span")
                print(cltree_span)

                start_index = cltree_span[0].i
                print("start_index")
                print(start_index)
            
                end_index = cltree_span[-1].i
                print("end_index")
                print(end_index)

                max_index = len(sentence)-1
                print("max_index")
                print(max_index)
                
                if end_index + 1 < max_index and sentence[end_index + 1].dep_ == 'punct':
                        cltree_str = sentence[start_index:end_index+2].text
                        cltree += [cltree_str]
                        usedIndex.append(end_index+1)
                else:
                        cltree_str = sentence[start_index:end_index+1].text
                        cltree += [cltree_str]

                print("cltree")
                print(cltree)
                print("usedIndex")
                print(usedIndex)
                
                atStart = any(word.is_sent_start for word in cltree_span)
                if atStart:
                  cltreeAtStart = cltree
                  cltree = []
                
               
                """cltree = str(cltree)
                print("string cltree")
                print(cltree)"""
                """for c in  word.children :
                    if c.is_sent_start:
                        cltreeAtStart = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                        found_sent_start = True
                        break
                  if not found_sent_start:
                    cltree_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    cltree += [cltree_str]"""
        if word.dep_ in( 'nsubjpass', 'csubjpass'):
                 #if word.head.dep_ == 'ROOT':
                    """subjpass_span = list(word.subtree)
                    print("subjpass_span")
                    print(subjpass_span)"""
                    
                    subjpass_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    if word.tag_ == 'WDT':
                      wsubjpass = subjpass_str
                    else:
                        subjpass = subjpass + subjpass_str
        if word.dep_ == 'nsubj': 
            subj = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
            #if word.head.dep_ == 'auxpass': 
            """if word.head.head.dep_ == 'ROOT': 
                    subjpass = subj """
        if word.dep_ == 'mark':
            if word.head.dep_ == 'ROOT':
                mark_str = word.text
                mark += [mark_str]
        if word.dep_ in ('advmod','npadvmod','oprd', 'amod'):
            if word.head.dep_ == 'ROOT':
                if word.is_sent_start:
                    adverb['start'] = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                elif verb == '':
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
            if word.head.dep_ in ('ROOT', 'relcl', 'advcl', 'xcomp', 'ccomp'):
                if word.dep_ == ('auxpass'):
                    aux += [word]
                else:                     
                     if(sentence[word.i+1].dep_ == 'auxpass') or (sentence[word.i+2].dep_ == 'auxpass'):
                          aux += [word]
        if word.dep_ == 'ROOT':
            verb = word.text
            verbLemma = word.lemma_
            if len(sentence) > word.i+1:
                if sentence[word.i+1].tag_ == 'IN' and sentence[word.i+1].dep_ != 'agent':
                    verbAddition = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in sentence[word.i+1].subtree).strip()
        if word.dep_ == 'prt':
            if word.head.dep_ == 'ROOT':
                part = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
        if word.dep_ == 'prep':
            #if word.head.dep_ in ('ROOT', 'auxpass'):
                prep_span = list(word.subtree)
                print("prep_span")
                print(prep_span)

                start_index = prep_span[0].i
                print("start_index")
                print(start_index)
            
                end_index = prep_span[-1].i
                print("end_index")
                print(end_index)

                max_index = len(sentence)-1
                print("max_index")
                print(max_index)
                
                if end_index + 1 < max_index and sentence[end_index + 1].dep_ == 'punct':
                        prep = sentence[start_index:end_index+2].text
                        #prep += [prep_str]
                else:
                        prep = sentence[start_index:end_index+1].text
                        #prep += [prep_str]

                print("prep")
                print(prep)
                
                atStart = any(word.is_sent_start for word in prep_span)
                if atStart:
                  prepAtStart = prep
                  prep = []
                
                  """if word.is_sent_start:
                    prepAtStart = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                  else:
                    prep_str = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                    prep += [prep_str]"""
            
        if word.dep_.endswith('obj'):
            if word.head.dep_ == 'agent':
                #if word.head.head.dep_ == 'ROOT':
                if word.head.head.dep_ in ('ROOT', 'relcl', 'advcl', 'xcomp', 'ccomp'):
                    agent = ''.join(w.text + ', ' if w.dep_=='appos' else (w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws) for w in word.subtree).strip()
                    aplural = word.tag_ in ('NNS','NNPS')
        if word.dep_ == "agent":
            agentExists = True
        if word.dep_ == 'cc':
            cconj = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree)
        if word.dep_ in ('xcomp'):
            if word.head.dep_ == 'ROOT':
                xcomp = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
                """Sthat = xcomp.startswith('that')
                xcomp = pass2act(xcomp, True).strip(' .')
                if not xcomp.startswith('that') and that:
                    xcomp = 'that '+xcomp"""
        if word.dep_ == 'punct':
            if word.text != '"':
                punc = word.text
        if word.dep_ in ('ccomp'):
            if word.head.dep_ == 'ROOT':
                ccomp = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
        if word.dep_ in ('conj'):
            if word.head.dep_ == 'ROOT':
                conj = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.subtree).strip()
    if not agentExists: # if no agent is found:
        agent = "one"
        aplural = False
    
    if aplural:
        aNumber = en.PLURAL
    if source != 'fileTransformation':
        print(f"subjpass: {subjpass}")
        print(f"subjpass-index: {wsubjpass}") #index???
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
        "wsubjpass": wsubjpass,
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
        "cconj": cconj,
        "xcomp": xcomp,
        "conj" : conj,
        "ccomp": ccomp,
        "mark": mark,
        "punc": punc
        }
    
    def get_subtree(index):
        subtree_span = list(sentence[index].subtree)
        for span_word in subtree_span:
                    if span_word.i not in usedIndex:
                        usedIndex.append(span_word.i)

        print(f"subtree_span:{sentence[index].text}")
        print(subtree_span)

        start_index = subtree_span[0].i
        print("start_index")
        print(start_index)
            
        end_index = subtree_span[-1].i
        print("end_index")
        print(end_index)

        max_index = len(sentence)-1
        print("max_index")
        print(max_index)
                
        if end_index + 1 < max_index and sentence[end_index + 1].dep_ == 'punct':
                    subtree = sentence[start_index:end_index+2].text
                    usedIndex.append(end_index+1)
        else:
                    subtree = sentence[start_index:end_index+1].text

        print(f"subtree: {sentence[index].text}")
        print(subtree)
        print("usedIndex")
        print(usedIndex)
                
        atStart = any(word.is_sent_start for word in subtree_span)
       
        return subtree, atStart
                
    
    def add_index():
        if word.i not in usedIndex:
                usedIndex.append(word.i)
         
    

    return results
