import stanza
import logging

# Deaktivating of the Stanza-logs otherwise too much unnecessary output is generated
logging.getLogger('stanza').setLevel(logging.WARNING) 

#stanza.download('en') # download English model


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma, depparse,constituency', download_method=None)
doc = nlp('A configurable device is a device that consists of several components which can be assembled by the manufacturer in multiple configurations.')

tree = doc.sentences[0].constituency
print("tree")
print(tree)
print("pretty print")
print(tree.pretty_print())
print("children")
print(tree.children[0].children[1])
print(tree.children[0].children[1].children[1])

print("SBAR")
"""for token in doc.sentences[0]:
    print(token.text)
    print(token.deprel)"""

for sent in doc.sentences:
    for word in sent.words:
        #if(word.deprel == ''):
        print(word.text, word.head, word.deprel, word.parent.text)

print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
if(tree.children[0].children[1] == 'SBAR'):
    print("SBAR")

def finde_passivsatz(sent):
    for word in sent.words:
        # Überprüfen, ob das Wort ein Hauptverb ist
        if word.deprel == 'root' and 'Verb' in word.upos:
            # Suchen nach auxpass und subjpass im Baum
            auxpass = any(child.deprel == 'aux:pass' for child in word.children)
            subjpass = any(child.deprel == 'nsubj:pass' for child in word.children)
            if auxpass and subjpass:
                return True
    return False

passiv_satzeile = [sent for sent in doc.sentences if finde_passivsatz(sent)]

print("passiv_satzeile")
print(passiv_satzeile)

""""
for sentence in doc.sentences:
    # Durchlaufen Sie die Konstituenten (Syntaktische Elemente) im Satz
    for constituency in sentence.constituency:
        # Überprüfen Sie, ob die Konstituente ein SBAR ist
        if 'SBAR' in constituency.text:
            # Drucken Sie die SBAR-Konstituente und ihre Kinder aus
            print("SBAR:", constituency.text)
            for child in constituency.children:
                print("Child:", child.text)"""
def finde_sbar(subtree):
    if subtree.label == 'SBAR':
        print("subtree")
        print(subtree.pretty_print())
        return subtree
    for child in subtree.children:
        result = finde_sbar(child)
        if result is not None:
            return result

sbar_subtree = None
for sent in doc.sentences:
    tree = sent.constituency
    sbar_subtree = finde_sbar(tree)
    if sbar_subtree:
        print("sbar_subtree")
        print(sbar_subtree)
        break
