def analyseSentence(sentence):

    for word in sentence:
        print(f"Text: {word.text}")
        print(f"Part of Speech: {word.pos_}") # POS Tagging
        print(f"Lemma: {word.lemma_}") # Lemmatization
        print(f"Dependency relation: {word.dep_}")  # Dependency Parsing
        print(f"Detailed POS tag: {word.tag_}")
        print(f"Is the word a punctuation: {word.is_punct}")
        print(f"Is the word a stop word: {word.is_stop}")
        print(f"Named entity type: {word.ent_type_}")    # Named Entity Recognition
        print(f"Does the word represent a number: {word.like_num}")
        print(f"morph: {word.morph}")


        print("\n")

      # Init parts of sentence to capture:
        subjpass = ''
        subj = ''
        verb = ''
        agent = ''
        #etc.

        for word in sentence:
            if word.dep_ == 'nsubjpass':
                subjpass = word.text
            if word.dep_ == 'nsubj':
                subj = word.text
            if word.dep_ == 'ROOT':
                verb = word.text   
            if word.dep_ == 'agent':
                agent = word.text 
                # etc.