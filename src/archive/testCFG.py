import nltk
from nltk import CFG
from nltk.parse import ChartParser

grammar = CFG.fromstring(
    """
    S -> NP VP
    VP -> V NP | V NP PP
    NP -> DT N | N
    PP -> P NP
    N -> 'NOUN'
    V -> 'VERB'
    P -> 'PREP'
    DT -> 'DET'
    ADJ -> 'ADJECTIVE'
    # ... other rules ...
"""
)

# Initialize parser
parser = ChartParser(grammar)

# Example POS-tagged sentence (output from a POS tagger)
tagged_sentence = [
    ("The", "DET"),
    ("quick", "ADJECTIVE"),
    ("brown", "ADJECTIVE"),
    ("fox", "NOUN"),
    ("jumps", "VERB"),
    ("over", "PREP"),
    ("the", "DET"),
    ("lazy", "ADJECTIVE"),
    ("dog", "NOUN"),
]

# Convert POS tags to CFG format
cfg_sentence = [
    (word, nltk.map_tag("en-ptb", "universal", tag)) for word, tag in tagged_sentence
]

# Parse the sentence
for tree in parser.parse([tag for word, tag in cfg_sentence]):
    tree.pretty_print()
