import pattern_patch 
import pattern.text.en as pat
import spacy
nlp = spacy.load("en_core_web_lg", disable=["ner", "parser", "tok2vec", "textcat", "attribute_ruler"])

#  verb conjugation
def conjugateVerb(data):
        verbLemma = data.get('verbLemma')
        tense = data.get('verbTense')
        aux = list(data.get('aux'))
        verbAspect = data.get('verbAspect')
        aux_doc = nlp(' '.join(aux))
        finalVerb = " "
       

        final_aux = ''
        num = pat.SINGULAR if not (data.get('aplural') or data.get('agent') in ('me', 'you', 'i')) else pat.PLURAL
        print("num")
        print(num)
        #aux.append(aux[0])s
        for (ll, l, c, n) in zip(aux_doc,aux_doc[1:],aux_doc[2:],aux_doc[3:]): #ll = last last, l = last, c = current, n = next
           
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
           if c.lemma_ == '.':
                continue

           if c.lemma_ == 'not':
                if l.lemma_ == 'be':
                    if n.lemma_ == 'be':
                        final_aux += pat.conjugate('be',tense=pat.tenses(l.text)[0][0],number=num) + ' '
                        verbAspect = pat.PROGRESSIVE
                    else:
                        final_aux += pat.conjugate('do',tense=pat.tenses(l.text)[0][0],number=num) + ' '
                elif l.lemma_ == 'have':
                    final_aux += pat.conjugate('have',tense=pat.tenses(l.text)[0][0],number=num) + ' '
                final_aux += 'not '
           elif c.lemma_ == 'be':
                if n.lemma_ == 'be':
                    print("progressive")
                    final_aux += pat.conjugate('be',tense=pat.tenses(c.text)[0][0],number=num) + ' '
                    verbAspect = pat.PROGRESSIVE
               
           elif c.lemma_ == 'have':
                num = pat.PLURAL if l.tag_ == 'MD' else num
                final_aux += pat.conjugate('have',tense=pat.tenses(c.text)[0][0],number=num) + ' '
                    #verbtense = pat.tenses(n.text)[0][0]
           elif c.tag_ == 'MD':
                num = pat.PLURAL
                final_aux += pat.conjugate(c.lemma_,tense=pat.tenses(n.text)[0][0],number=num) + ' '
                    #verbtense = pat.tenses(n.text)[0][0]
           else:
                final_aux += c.text_with_ws
        final_aux = final_aux.lower().strip()    

         # conjugate main verb:
        if verbAspect:
            verbActive = pat.conjugate(verbLemma,tense=tense,aspect=verbAspect, number=num)
        else:
            verbActive = pat.conjugate(verbLemma,tense=tense, number=num)

        if final_aux is not None and verbActive is not None:
            if final_aux == '':
                finalVerb =  verbActive
            else:
                finalVerb = final_aux + " " + verbActive
        else:
            print("One is NONE")
            print("final_aux")
            print(final_aux)
            print("verbActive")
            print(verbActive)
        return finalVerb


    