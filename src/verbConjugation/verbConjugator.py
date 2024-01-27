import pattern_patch
import pattern.text.en as pat
import spacy

# Load NLP model
try:
    nlp = spacy.load("en_core_web_lg")
except Exception as e:
    spacy.cli.download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")


#  verb conjugation
def conjugateVerb(data):
    """
    This function takes the data from the sentence analysis and conjugates the verb accordingly.

    Input: the output of the sentence analysis
    Steps:
    1. Get the data from the sentence analysis
    2. Iterate through the auxilary verbs and conjugate them according to time, person and number
    3. Check if there is a modal auxilary verb in the sentence and adapt negations accordingly
    4. Conjugate main verb in active form
    Output: the conjugated verb
    """
    # get data from analyseSentence
    verbLemma = data.get("verbLemma")
    tense = data.get("verbTense")
    aux = list(data.get("aux"))
    verbAspect = data.get("verbAspect")
    aux_doc = nlp(" ".join(aux))
    finalVerb = {"auxilaryVerb": "", "activeVerb": ""}
    finalAux = []
    num = (
        pat.SINGULAR
        if not (data.get("aplural") or data.get("agent") in ("me", "you", "i"))
        else pat.PLURAL
    )

    # Iterate through the auxilary verbs and conjugate them according to time, person and number
    for ll, l, c, n in zip(
        aux_doc, aux_doc[1:], aux_doc[2:], aux_doc[3:]
    ):  # ll = last last, l = last, c = current, n = next
        print("ll")
        print(ll)
        print("l")
        print(l)
        print(l.tag_)
        print("c")
        print(c)
        print(c.tag_)
        print("n")
        print(n)
        print(n.tag_)
        print("finalaux")
        print(finalAux)

        try:
            if c.lemma_ == ".":
                continue

            if n.lemma_ == "not":
                print("n.lemma")
                print(n.lemma_)
                if l.lemma_ == "be":
                    if n.text == "being":
                        finalAux.append(
                            pat.conjugate(
                                "be", tense=pat.tenses(l.text)[0][0], number=num
                            )
                        )
                        verbAspect = pat.PROGRESSIVE
                    else:
                        finalAux.append(
                            pat.conjugate(
                                "do", tense=pat.tenses(l.text)[0][0], number=num
                            )
                        )

                elif l.lemma_ == "have":
                    finalAux.append(
                        pat.conjugate(
                            "have", tense=pat.tenses(l.text)[0][0], number=num
                        )
                    )

                elif c.lemma_ == "have":
                    num = pat.PLURAL if l.tag_ == "MD" else num
                    if num == "singular":
                        print("third person")
                        print(pat.tenses(c.text)[0][0])
                        if pat.tenses(c.text)[0][0] == "infinitive":
                            finalAux.append(
                                pat.conjugate(
                                    "have", tense="present", person=3, number=num
                                )
                            )
                        else:
                            finalAux.append(
                                pat.conjugate(
                                    "have",
                                    tense=pat.tenses(c.text)[0][0],
                                    person=3,
                                    number=num,
                                )
                            )
                    else:
                        finalAux.append(
                            pat.conjugate(
                                "have", tense=pat.tenses(c.text)[0][0], number=num
                            )
                        )
                elif c.tag_ == "MD" or c.lemma_ == "will":
                    num = pat.PLURAL
                    finalAux.append(
                        pat.conjugate(
                            c.lemma_, tense=pat.tenses(n.text)[0][0], number=num
                        )
                    )

                finalAux.append("not")

            elif c.lemma_ == "be":
                if n.text == "being":
                    print("progressive")
                    finalAux.append(
                        pat.conjugate("be", tense=pat.tenses(c.text)[0][0], number=num)
                    )
                    verbAspect = pat.PROGRESSIVE

            elif c.lemma_ == "have":
                num = pat.PLURAL if l.tag_ == "MD" else num
                if num == "singular":
                    print("third person")
                    print(pat.tenses(c.text)[0][0])
                    if pat.tenses(c.text)[0][0] == "infinitive":
                        finalAux.append(
                            pat.conjugate("have", tense="present", person=3, number=num)
                        )
                    else:
                        finalAux.append(
                            pat.conjugate(
                                "have",
                                tense=pat.tenses(c.text)[0][0],
                                person=3,
                                number=num,
                            )
                        )
                else:
                    finalAux.append(
                        pat.conjugate(
                            "have", tense=pat.tenses(c.text)[0][0], number=num
                        )
                    )

            elif c.tag_ == "MD" or c.lemma_ == "will":
                num = pat.PLURAL
                if c.text == "could":
                    finalAux.append("could")
                else:
                    finalAux.append(
                        pat.conjugate(
                            c.lemma_, tense=pat.tenses(n.text)[0][0], number=num
                        )
                    )
            else:
                if c.lemma_ != "not":
                    finalAux.append(c.text)
        except Exception as e:
            print(
                f"There has accured the following error during conjugating the auxilarly verbs: {e}"
            )
            raise

    # check if there is a modal auxilary verb in the sentence and adapt negations accordingly
    modal_aux_verbs = [
        "should",
        "would",
        "could",
        "have",
        "shall",
        "will",
        "may",
        "might",
        "must",
    ]
    for index, element in enumerate(finalAux):
        if any(element in modal_aux_verbs for element in finalAux):
            break
        elif element == "not" and num == pat.SINGULAR:
            finalAux[index] = "does not"
            num = pat.PLURAL
        elif element == "not" and num == pat.PLURAL:
            finalAux[index] = "do not"

    finalAux = " ".join(finalAux)
    finalAux.lower().strip()
    print("finalAux")
    print(finalAux)

    try:
        # Conjugate main verb in active form
        if verbAspect:
            verbActive = pat.conjugate(
                verbLemma, tense=tense, aspect=verbAspect, number=num
            )
        else:
            verbActive = pat.conjugate(verbLemma, tense=tense, number=num)

        if finalAux is not None and verbActive is not None:
            finalVerb["auxilaryVerb"] = finalAux
            finalVerb["activeVerb"] = verbActive
            print("finalAux")
            print(finalAux)
            print("verbActive")
            print(verbActive)
        else:
            print("One is NONE")
            print("finalAux")
            print(finalAux)
            print("verbActive")
            print(verbActive)
    except Exception as e:
        print(
            f"There has accured the following error during conjugating the active verb: {e}"
        )
        raise

    return finalVerb
