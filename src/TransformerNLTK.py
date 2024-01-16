
import nltk
from nltk import CFG
import nltk
import parsingPOSTagging.sentenceParserTest as analyseSentenceTest



nltk.download('punkt')  # Download the necessary datasets


sentence = "The quick brown fox jumps over the lazy dog."
tokens = nltk.word_tokenize(sentence)
print(tokens)
nltk.download('averaged_perceptron_tagger')  # Download the POS tagger

pos_tags = nltk.pos_tag(tokens)
print("POS Tags:", pos_tags)
nltk.download('maxent_ne_chunker')
nltk.download('words')

ner_tree = nltk.ne_chunk(pos_tags)
print("NER Tree:", ner_tree)

# Stellen Sie sicher, dass der NLTK CoreNLPParser auf den Stanford CoreNLP Server zugreift
# Dies setzt voraus, dass Stanford CoreNLP lokal ausgeführt wird
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

    print("preClause")
    print(preClause)
    print("postClause")
    print(postClause)

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
    last_component = final_components[-1]

    # if last elements ends with a punctuation mark or whitespace, remove it
    if final_components[-1][-1] in ('.', '?', '!', ',', ':', ';', ' '):
       ("final components schleife")
       final_components[-1] = final_components[-1][:-1]
    
    
    print(final_components[-1][-1])

    print("final components:")
    print(final_components)
    
    finalClause =  " ".join(final_components) + punc
    if preClause and preClause != 'false':
      finalClause = preClause + " " + finalClause
    if postClause and postClause != 'false':
      if postClause == '.':
        finalClause = finalClause + postClause 
      else:
          finalClause = finalClause + " " + postClause
    
    
    finalClause = finalClause[0].upper() + finalClause[1:]
   
    print(finalClause)

    return finalClause

    subject = subjpass   
    VP1 = "V V PP"

    grammar1 = CFG.fromstring(f"""
        S -> NP VP
        NP -> Det N
        VP -> V NP | {VP1}
        PP -> P N
        Det -> 'The' | 'the'
        N -> 'ball' | '{subject}'
        V -> 'thrown' | 'was'
        P -> 'by'
    """)

    parser = nltk.ChartParser(grammar1)

    sentence = "The ball was thrown by John".split()
    trees = list(parser.parse(sentence))
    print("trees")
    print(trees)
    print(trees[0])
    print("Schleife")
    if not trees:
        print("No valid parse trees.")
    else:
        for tree in trees:
            print(tree)

    def pattern1(parsed_tree):
        # This is a simplified logic, actual implementation might need to handle more cases
            subject = parsed_tree[1][2][1][0] # Assuming 'John'
            verb = "threw"  # getting it from pattern
            obj = f'{parsed_tree[0][0][0]} {parsed_tree[0][1][0]}' # Assuming 'the ball'

            return f"{subject} {verb} {obj}"

    # Assuming 'trees[0]' is the correct parse tree
    active_sentence = pattern1(trees[0])
    print("active_sentence")
    print(active_sentence)

    """


    parser = CoreNLPParser(url='http://localhost:5000')

    # Parsen Sie einen Satz
    sentence = "The quick brown fox jumps over the lazy dog."
    parse = next(parser.raw_parse(sentence))

    # Dependency Tree zeichnen
    parse.pretty_print()

    """