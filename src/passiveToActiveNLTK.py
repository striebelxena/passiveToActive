
import nltk
from nltk.parse import CoreNLPParser

# Stellen Sie sicher, dass der NLTK CoreNLPParser auf den Stanford CoreNLP Server zugreift
# Dies setzt voraus, dass Stanford CoreNLP lokal ausgeführt wird
parser = CoreNLPParser(url='http://localhost:5000')

# Parsen Sie einen Satz
sentence = "The quick brown fox jumps over the lazy dog."
parse = next(parser.raw_parse(sentence))

# Dependency Tree zeichnen
parse.pretty_print()
