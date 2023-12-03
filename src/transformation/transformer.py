# Assuming a simple structure for demonstration purposes
if is_passive:
    subject = ""
    agent = ""
    verb = ""
    for token in doc:
        if token.dep_ == "nsubjpass":
            agent = token.head.text
        elif token.dep_ == "agent":
            subject = ''.join([child.text for child in token.children if child.dep_ == "pobj"])
        if token.pos_ == "VERB":
            verb = token.text

    # Basic conversion (not considering verb tense adjustments)
    active_sentence = f"{subject} {verb} {agent}"
    print(f"Active Sentence: {active_sentence}")
