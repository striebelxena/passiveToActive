import composition.nounInversion as ni


def transformSentence(data, finalVerb, preClause, postClause):
    """
    This function transforms the sentence by combining the seperate parts
    Input: data of the sentence analyses, the active verb, the preClause and the postClause
    Steps:
    1. Get the components of the sentence
    2. Inverse the agent if it is not "one"
    3. Combine the components to a new sentence
    4. Filter out empty components
    5. Combine the components to a new sentence and put it between the pre and post clause
    Output: to active voice transformed sentence and the length of the new sentence

    """
    # Get the components of the sentence
    verb = finalVerb["activeVerb"].strip()
    auxilary = finalVerb["auxilaryVerb"].strip()
    agent = data.get("agent")
    subjpass = ni.inversion(data.get("subjpass"))
    adverbStart = data.get("adverb")["start"]
    adverbBefore = data.get("adverb")["bef"]
    adverbAfter = data.get("adverb")["aft"]
    cltreeAtStart = data.get("cltreeAtStart")
    cltree = data.get("cltree")
    cltree = " ".join(cltree)
    prepAtStart = data.get("prepAtStart")
    prep = data.get("prep")
    prep = " ".join(prep)
    xcomp = data.get("xcomp")
    ccomp = data.get("ccomp")
    conj = data.get("conj")
    part = data.get("part")
    verbAddition = data.get("verbAddition")
    wsubj = data.get("wsubjpass")
    mark = data.get("mark")
    mark = " ".join(mark)
    preClause = str(preClause)
    postClause = str(postClause)
    finalClause = ""

    # Inverse the agent if it is not "one"
    if agent != "one":
        agent = ni.inversion(agent)

    subject = agent
    object = subjpass

    try:
        # All components of the new sentence
        components = [
            mark,
            adverbStart,
            prepAtStart,
            cltreeAtStart,
            wsubj,
            subject,
            auxilary,
            adverbBefore,
            verb,
            part,
            object,
            verbAddition,
            adverbAfter,
            cltree,
            prep,
            xcomp,
            ccomp,
            conj,
        ]
        components = [comp for comp in components if comp]

        # Filter out empty components
        filtered_components = [comp for comp in components if comp]

        final_components = filtered_components

        # If last elements ends with a punctuation mark or whitespace, remove it
        if final_components[-1][-1] in (".", "?", "!", ",", ":", ";", " "):
            ("final components schleife")
            final_components[-1] = final_components[-1][:-1]

        if postClause.endswith("."):
            postClause = postClause[:-1]

        finalClause = " ".join(final_components).split()
        newLength = len(finalClause)

        finalClause = " ".join(finalClause)
        finalActiveSubclause = finalClause

        # Combine the components to a new sentence and put it between the pre and post clause
        if preClause and preClause != "false":
            finalClause = preClause + " " + finalClause
        if postClause and postClause != "false":
            if postClause == ".":
                finalClause = finalClause
            elif postClause.startswith(","):
                finalClause = finalClause + postClause
            else:
                finalClause = finalClause + " " + postClause

        finalClause = finalClause[0].upper() + finalClause[1:]

    except Exception as e:
        print(f"There occured the following error during forming the new sentence: {e}")
        raise

    return finalClause, finalActiveSubclause, newLength
