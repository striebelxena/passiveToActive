
import nltk
from nltk import CFG
import nltk
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

subject = "John"    
VP1 = "V V PP"

grammar = CFG.fromstring(f"""
    S -> NP VP
    NP -> Det N
    VP -> V NP | {VP1}
    PP -> P N
    Det -> 'The' | 'the'
    N -> 'ball' | '{subject}'
    V -> 'thrown' | 'was'
    P -> 'by'
""")

parser = nltk.ChartParser(grammar)

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

def transform_passive_to_active(parsed_tree):
    # This is a simplified logic, actual implementation might need to handle more cases
        subject = parsed_tree[1][2][1][0] # Assuming 'John'
        verb = "threw"  # getting it from pattern
        obj = f'{parsed_tree[0][0][0]} {parsed_tree[0][1][0]}' # Assuming 'the ball'

        return f"{subject} {verb} {obj}"

# Assuming 'trees[0]' is the correct parse tree
active_sentence = transform_passive_to_active(trees[0])
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