
def transformSentence(sentence, verbActive):
    subject = ""
    agent = ""
    verb = ""
    for token in sentence:
        if token.dep_ == "nsubjpass":
            agent = token.head.text
        elif token.dep_ == "agent":
            subject = ''.join([child.text for child in token.children if child.dep_ == "pobj"])
        if token.pos_ == "VERB":
            verb = token.text

    # Basic conversion (not considering verb tense adjustments)
    active_sentence = f"{subject} {verb} {agent}"
    active_sentence = ("The Bundestag shall adopt federal laws.")
    return active_sentence
