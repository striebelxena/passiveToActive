def checkForPassive(sentence):
    for word in sentence:
        print(word)
        print(word.dep_)
        print(word.tag_)
        # has_auxpass = any(word.dep_ == "auxpass" for word in sentence)
        # has_nsubjpass = any(word.dep_ == "nsubjpass" for word in sentence)
        # passiveClause = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.head.subtree).strip()

        # if has_auxpass and has_nsubjpass:
        #             passiveSentences.append(subclause)

        if word.dep_ in ("nsubjpass", "csubjpass"):
            print(word)
            """for word in sentence:
                if word.dep_ == 'auxpass': 
                  print(word.head.subtree)
                  passiveClause = ''.join(w.text_with_ws.lower() if w.tag_ not in ('NNP','NNPS') else w.text_with_ws for w in word.head.subtree).strip()
                  print("passiveClause")
                  print(passiveClause)
                  return passiveClause
    return False"""
            auxpass_tokens = [w for w in sentence if w.dep_ == "auxpass"]
            print("auxpass_tokens")
            print(auxpass_tokens)
            if auxpass_tokens:
                subtree_span = list(auxpass_tokens[0].head.subtree)
                print("subtree_span")
                print(subtree_span)
                start_index = subtree_span[0].i
                end_index = subtree_span[-1].i
                passiveClause = sentence[start_index : end_index + 1]
                preClause = sentence[:start_index]
                postClause = sentence[end_index + 1 :]
                print("Passive Clause:", passiveClause)
                print("Start Index:", start_index, "End Index:", end_index)
                print("Pre Clause:", preClause)
                print("Post Clause:", postClause)
                return passiveClause, preClause, postClause
    return False, False, False
