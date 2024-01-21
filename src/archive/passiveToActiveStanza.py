import stanza
import logging
from collections import deque
from graphviz import Digraph
import nltk
from nltk import CFG
import nltk

# Deaktivating of the Stanza-logs otherwise too much unnecessary output is generated
logging.getLogger('stanza').setLevel(logging.WARNING) 

#stanza.download('en') # download English model


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma, depparse,constituency', download_method=None)
doc = nlp('It shall be convened by the President of the Bundestag. ')
tree = doc.sentences[0].constituency
endpoints = {}


def traverse_constituency_tree(node, parent_label=None):
    if not node.children:  # Überprüft, ob es sich um einen Blattknoten handelt
        print(f"Word: {node.label}, POS: {parent_label}")
        if parent_label in endpoints:
            # Wenn es bereits einen Eintrag für das POS-Tag gibt, fügen Sie das Wort hinzu
            endpoints[parent_label] = f"{endpoints[parent_label]}| {node.label}"
        else: 
            endpoints[parent_label] =  node.label
        print("endpoints")
        print(endpoints)
    else:
        # Für nicht-Blattknoten
        for child in node.children:
            traverse_constituency_tree(child, parent_label=node.label)

traverse_constituency_tree(tree)


grammar2 = CFG.fromstring(f"""
        S -> NP VP
        NP -> Det N | N | PRP | NNP |NP PP| Det NNP
        VP ->  MD VP | V | VB VP | VBN PP | V NP NP PP | V NP PP PP | V NP NP PP PP | V NP NP NP | V NP NP NP PP | V NP NP NP NP | V NP NP NP NP PP | V NP NP NP NP NP | V NP NP NP NP NP PP | V NP NP NP NP NP NP | V NP NP NP NP NP NP PP | V NP NP NP NP NP NP NP | V NP NP NP NP NP NP NP PP | V NP NP NP NP NP NP NP NP | V NP NP NP NP NP NP NP NP PP | V NP NP NP NP NP NP NP NP NP | V NP NP NP NP NP NP NP NP NP PP | V NP NP N
        PP -> IN NP 
        Det -> 'The' | 'the'
        PRP -> '{endpoints["PRP"]}'
        MD -> '{endpoints["MD"]}'
        VB -> '{endpoints["VB"]}'
        VBN ->'{endpoints["VBN"]}'
        IN -> '{endpoints["IN"]}'
    """)


parser = nltk.ChartParser(grammar2)
sentence = "It shall be convened by the President of the Bundestag.".split()
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





"""for node in node.children:

    if len(node.children) == 1:  
     # Überprüft, ob es sich um einen Blattknoten handelt
        # Direktes Kind des aktuellen Knotens ist das Wort
        for  word in node.children:
            #word = node.children[0]
            print(f"Word: {word.label}, POS: {node.label}")
    else:
        # Für nicht-Blattknoten
        for child in node.children:
            traverse_constituency_tree(child)
            print(f"Phrase: {node.label}")"""
    	



print("tree")
print(tree)
print("pretty print")
print(tree.pretty_print())
print("children")
print(tree.children[0].children[1])
#print(tree.children[0].children[1].children[1])

endpunkte = {}

def finde_endpunkte(node, endpunkte):
    
    if not node.children:  # Wenn der Knoten keine Kinder hat, ist es ein Blatt
            label = node.label
            print("label")
            print(label)
            endpunkte[label] = node
    
    else:
        for child in node.children:
            finde_endpunkte(child, endpunkte)



# Initialisieren Sie ein Wörterbuch, um die Endpunkte zu speichern

# Starten Sie die Suche vom Wurzelknoten
finde_endpunkte(tree, endpunkte)

# Ausgabe der gefundenen Endpunkte
print("endpunkte")
print(endpunkte)
print("ende Endpunkte")

""""
def walk_tree(node):
    print(node.label)
    for child in node.children:
        walk_tree(child)

# Angenommen, 'tree' ist Ihr Syntaxbaum
walk_tree(tree)

print("get_level_2_subtrees")
def get_level_2_subtrees(root):
    queue = deque([root])
    level = 0
    level_2_subtrees = []

    while queue and level < 3:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if level == 2:  # Wir sind auf der zweiten Ebene (level 1, da wir bei 0 beginnen)
                level_2_subtrees.append(node)
            queue.extend(node.children)
        level += 1

    return level_2_subtrees

# Angenommen, 'tree' ist Ihr Syntaxbaum
level_2_subtrees = get_level_2_subtrees(tree)
for subtree in level_2_subtrees:
    print(subtree.label) 

print("SBAR")"""
"""for token in doc.sentences[0]:
    print(token.text)
    print(token.deprel)"""
"""
for sent in doc.sentences:
    for word in sent.words:
        #if(word.deprel == ''):
        print(word.text, word.head, word.head, word.deprel, word.parent)

print(*[f'id: {word.id}\tword: {word.text} \thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
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
print(passiv_satzeile)"""

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
"""def finde_sbar(subtree):
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

"""