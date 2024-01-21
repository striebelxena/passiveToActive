# import spacy


def checkForPassive(sentence):
    """
    This function checks if the sentence is passive by checking if the dependency is a passive subject and if there is an auxilarry verb in passive
    It splits the sentence into pre, post and passive clause, saves all identified passive constructions and its components in a list
    Also it saves the position of the passive construction in the original
    Finally, it returns  the list of passive constructions, the list of pre clauses, the list of post clauses and the list of indices of the passive constructions in the original sentence

    """
    preClause = list()
    postClause = list()
    passiveClause = []
    indicesOfSubtrees = []
    for word in sentence:
        # check if the sentence is passive by checking if the dependency is a passive subject and if there is an auxilarry verb in passive
        try:
            if word.dep_ in ("nsubjpass", "csubjpass"):
                auxpass_tokens = [
                    w
                    for w in sentence
                    if w.dep_ == "auxpass"
                    and (w.i == 0 or sentence[w.i - 1].lower_ != "to")
                ]
                print("auxpass_tokens")
                print(auxpass_tokens)

                if auxpass_tokens:
                    for token in auxpass_tokens:
                        subtree_span = list(token.head.subtree)
                        start_index = subtree_span[0].i
                        end_index = subtree_span[-1].i
                        passiveClause.append(sentence[start_index : end_index + 1])
                        preClause.append(sentence[:start_index])
                        postClause.append(sentence[end_index + 1 :])
                        indicesOfSubtrees.append(f"{start_index},{end_index} ")
                        print("iteration:", token)
                        print("Passive Clause:", passiveClause)
                        print("Start Index:", start_index, "End Index:", end_index)
                        print("Pre Clause:", preClause)
                        print("Post Clause:", postClause)
        except Exception as e:
            print(
                f"There has been the following error in checking whether the sentence has passive constructions: {e}"
            )
            raise

            return passiveClause, preClause, postClause, indicesOfSubtrees
    return False, False, False, False
