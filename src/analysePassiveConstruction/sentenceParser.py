import spacy
import pattern.text.en as en

nlp = spacy.load("en_core_web_lg")


def analyseSentence(sentence):
    """
    Input: Sentence with a passive construction as a spacy object

    Analysis of the sentence structure and the parts of the sentence
    Steps:
    1. Iterates over the words in the sentence and assigns the parts of the sentence to the corresponding variables
    2. Identifies characteristics of the verb like tense, person, mood, aspect, form for later conjugation into active
    3. Creates a dictionary with the parts of the sentence

    Output: Dictionary with the parts of the sentence
    """

    # Init parts of sentence to capture:
    subjpass = ""
    subj = ""
    verb = ""
    verbTense = ""
    verbPerson = "1"
    verbMood = ""
    verbAspect = ""
    verbAddition = ""
    verbForm = ""
    adverb = {"start": "", "bef": "", "aft": ""}
    part = ""
    prepAtStart = ""
    prep = list()
    mark = list()
    agent = ""
    agentExists = False
    aplural = False
    aNumber = en.SINGULAR
    cltreeAtStart = ""
    cltree = list()
    aux = list(list(nlp(". .").sents)[0])  # start with 2 'null' elements
    cconj = ""
    xcomp = ""
    conj = ""
    ccomp = ""
    punc = ""
    wsubjpass = ""
    usedIndex = []
    signIndex = 0
    setenceString = str(sentence)

    def get_subtree(index):
        """
        Input: Index of the current word in the sentence as integer
        Steps:
        1. Get the subtree of the word and save indices of each word of the subtree in a list, to track the words that have already been "used"
        2. Handle punctuation
        3. Handle capitalization
        4. Handle sentence start

        Output: Subtree, if it is at the start of the sentence and the start index of the subtree
        """
        try:
            subtree_span = list(sentence[index].subtree)
            for span_word in subtree_span:
                if span_word.i not in usedIndex:
                    usedIndex.append(span_word.i)

            start_index = subtree_span[0].i

            end_index = subtree_span[-1].i

            max_index = len(sentence) - 1

            if end_index + 1 < max_index and sentence[end_index + 1].text in (
                ",",
                ";",
                ":",
                "(",
                ")",
                "[",
                "]",
                "{",
                "}",
                '"',
                "'",
            ):
                subtree = sentence[start_index : end_index + 2].text
                usedIndex.append(end_index + 1)
            else:
                subtree = sentence[start_index : end_index + 1].text

            subtree = subtree.strip()
            if (
                start_index == 0
                and sentence[start_index].pos_ != "PROPN"
                and sentence[start_index].ent_type_
                not in (
                    "PERSON",
                    "ORG",
                    "GPE",
                    "LOC",
                    "LANGUAGE",
                    "NORP",
                    "FAC",
                    "DATE",
                    "TIME",
                )
            ):
                subtree = subtree[0].lower() + subtree[1:]

            atStart = any(word.is_sent_start for word in subtree_span)

        except Exception as e:
            print(f"There has been the following error in getting the subtree: {e}")
            raise

        return subtree, atStart, start_index

    def add_index(index):
        """
        Input: Index of the current word in the sentence as integer
        Add the index to the list of used indices
        """
        if index not in usedIndex:
            usedIndex.append(index)

    def used_index(index):
        """
        Input: Index of the current word in the sentence as integer

        Check if the index is already in the list of used indices
        Output: True if the index is already in the list of used indices, False otherwise
        """
        if index in usedIndex:
            return True
        else:
            return False

    # Iterate over the words in the sentence and assign the parts of the sentence to the corresponding variables
    for word in sentence:
        print(f"word: {word}")
        print(f"dep: {word.dep_}")
        print(f"tag: {word.tag_}")

        try:
            # Check if the word has already been used/analysed
            if word.i not in usedIndex:
                # Check if the word is the head of a subclause
                if word.dep_ in ("acl", "advcl", "relcl"):
                    if word.head.dep_ in ("ROOT", "auxpass"):
                        subtree, atStart, startIndex = get_subtree(word.i)
                        if atStart:
                            cltreeAtStart = subtree
                        else:
                            cltree += [subtree]

                # Check if the word is a passive subject or clause
                if word.dep_ in ("nsubjpass", "csubjpass"):
                    subtree, atStart, startIndex = get_subtree(word.i)
                    # Check if the word is a w-word (who, what, where, when, why, how, that)
                    if (
                        word.tag_ == "WDT"
                        or word.tag_ == "WP"
                        or word.tag_ == "WP$"
                        or word.text == "that"
                    ):
                        wsubjpass = subtree
                    # Check if the word is a noun assign it appropriately to the variable
                    elif subjpass == "":
                        subjpass = subtree
                    elif verb == "":
                        signIndex = sentence[startIndex].idx - 1
                        if setenceString[signIndex] != " ":
                            subjpass = subjpass + subtree
                        else:
                            subjpass = subjpass + " " + subtree

                # Check if the word is a subject
                if word.dep_ == "nsubj":
                    subtree, atStart, startIndex = get_subtree(word.i)
                    subj = subj + subtree

                # Check if the word is a mark
                if word.dep_ == "mark":
                    if word.head.dep_ == "ROOT":
                        add_index(word.i)
                        mark_str = word.text
                        mark += [mark_str]

                # Check if the word is an adverb
                if word.dep_ in ("advmod", "npadvmod", "oprd", "amod"):
                    if word.head.dep_ == "ROOT":
                        if word.is_sent_start:
                            subtree, atStart, startIndex = get_subtree(word.i)
                            adverb["start"] = subtree
                        elif verb == "":
                            subtree, atStart, startIndex = get_subtree(word.i)
                            adverb["bef"] = subtree
                        else:
                            subtree, atStart, startIndex = get_subtree(word.i)
                            if adverb["aft"] == "":
                                adverb["aft"] = subtree
                            else:
                                adverb["aft"] = adverb["aft"] + " " + subtree

                # Check if the word is an auxiliary verb for a passive construction
                # According to the auxiliary verb, assign the tense, person, mood, aspect and form of the verb
                if word.dep_ == "auxpass":
                    if word.head.dep_ == "ROOT":
                        # verbForm = word.morph.get("VerbForm")
                        if sentence[word.i - 1].lemma_ == "have":
                            verbAspect = en.PARTICIPLE
                            verbTense = en.PAST
                            # verbForm = en.PARTICIPLE
                        if sentence[word.i - 1].lemma_ == "will":
                            verbTense = en.PRESENT
                        elif word.tag_ == "VBZ":  # 3rd person singular
                            verbPerson = en.THIRD
                            verbTense = en.PRESENT
                        elif word.tag_ == "VB":
                            verbTense = (
                                en.PRESENT
                            )  # if auxpass is infinitive, the active verb should be present
                        elif word.tag_ == "VBD":
                            verbTense = en.PAST
                        elif word.tag_ == "VBG":
                            verbTense = en.PRESENT
                            verbAspect = en.PROGRESSIVE
                        elif word.tag_ == "VBN":
                            verbTense = en.PAST
                        elif word.tag_ == "VBP" or word.tag_ == "VBZ":
                            verbTense = en.PRESENT
                        elif word.tag_ == "MD":
                            verbTense = en.PRESENT
                        else:
                            verbTense = en.tenses(word.text)[0][0]

                # Check if the word is a auxiliary verb or negation
                if word.dep_ in ("aux", "auxpass", "neg"):
                    if word.head.dep_ in (
                        "ROOT"
                    ):  # "relcl", "advcl", "xcomp", "ccomp"):
                        if word.dep_ == ("auxpass"):
                            add_index(word.i)
                            aux += [word]
                        else:
                            if (
                                (sentence[word.i - 1].dep_ == "auxpass")
                                or (sentence[word.i + 1].dep_ == "auxpass")
                                or (sentence[word.i + 2].dep_ == "auxpass")
                            ):
                                add_index(word.i)
                                aux += [word]

                # Check if the word is a the main verb (ROOT) of the construction
                if word.dep_ == "ROOT":
                    verb = word.text
                    add_index(word.i)
                    verbLemma = word.lemma_
                    # Check if the verb is extended by an addition
                    if len(sentence) > word.i + 1:
                        if used_index(word.i + 1) == False:
                            if (
                                sentence[word.i + 1].tag_ == "IN"
                                and sentence[word.i + 1].dep_ != "agent"
                            ):
                                subtree, atStart, startIndex = get_subtree(word.i + 1)
                                verbAddition = subtree
                            elif sentence[word.i + 1].dep_ == "oprd":
                                subtree, atStart, startIndex = get_subtree(word.i + 1)
                                verbAddition = subtree
                            elif sentence[word.i + 1].head.dep_ == "oprd":
                                head_index = sentence[word.i + 1].head.i
                                subtree, atStart, startIndex = get_subtree(head_index)
                                verbAddition = subtree

                # Check if the word is a participle
                if word.dep_ == "prt":
                    if word.head.dep_ == "ROOT":
                        subtree, atStart, startIndex = get_subtree(word.i)
                        part = subtree

                # Check if the word is a preposition
                if word.dep_ == "prep":
                    # if word.head.dep_ in ('ROOT', 'auxpass'):
                    subtree, atStart, startIndex = get_subtree(word.i)
                    prep_str = subtree
                    if atStart:
                        prepAtStart = prep_str
                    else:
                        prep += [prep_str]

                # Check if the word is a passive agent and get number of agent
                if word.dep_.endswith("obj"):
                    if word.head.dep_ == "agent":
                        if word.head.head.dep_ in (
                            "ROOT",
                            "relcl",
                            "advcl",
                            "xcomp",
                            "ccomp",
                        ):
                            subtree, atStart, startIndex = get_subtree(word.i)
                            agent = subtree
                            aplural = word.tag_ in ("NNS", "NNPS")

                if word.dep_ == "agent":
                    agentExists = True

                # Check if the word is a conjunction
                if word.dep_ == "cc":
                    subtree, atStart, startIndex = get_subtree(word.i)
                    cconj = subtree

                # Check if the word is a xcomp
                if word.dep_ in ("xcomp"):
                    if word.head.dep_ == "ROOT":
                        subtree, atStart, startIndex = get_subtree(word.i)
                        xcomp = subtree

                # Check if the word is a ccomp
                if word.dep_ in ("ccomp"):
                    if word.head.dep_ == "ROOT":
                        subtree, atStart, startIndex = get_subtree(word.i)
                        ccomp = subtree

                # Check if the word is a punctuation
                if word.dep_ == "punct":
                    if word.text != '"':
                        punc = word.text
                        add_index(word.i)

                # Check if the word is a conjunction
                if word.dep_ in ("conj"):
                    if word.head.dep_ == "ROOT":
                        subtree, atStart, startIndex = get_subtree(word.i)
                        conj = subtree
        except Exception as e:
            print(f"There has been the following error in analysing the sentence: {e}")
            raise

            # End of the iteration through the words in the sentence

    # If no agent has been found assign as default agent "one"
    if not agentExists:
        agent = "one"
        aplural = False

    if aplural:
        aNumber = en.PLURAL

    # Create a dictionary with the parts of the sentence
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
        "prepAtStart": prepAtStart,
        "prep": prep,
        "agent": agent,
        "aplural": aplural,
        "aNumber": aNumber,
        "cltreeAtStart": cltreeAtStart,
        "cltree": cltree,
        "aux": [a.text for a in aux],
        "verbAddition": verbAddition,
        "cconj": cconj,
        "xcomp": xcomp,
        "conj": conj,
        "ccomp": ccomp,
        "mark": mark,
        "punc": punc,
    }
    print(f"results: {results}")

    return results
