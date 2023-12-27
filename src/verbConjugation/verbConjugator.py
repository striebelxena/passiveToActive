import pattern_patch 
import pattern.text.en as pat
import spacy
nlp = spacy.load("en_core_web_lg")



#verbActive = en.conjugate("follow", "past", 1, "singular") #need to be like this!!!!




#  verb conjugation
def conjugateVerb(data, verbLemma, tense, aux, number):
        aux = list(data.get('aux'))
        aux_doc = nlp(' '.join(aux))
        print("aux_doc")
        print(aux_doc)
        finalVerb = " "
        person = data.get('verbPerson')
        print("person") 
        print(person)
        

        final_aux = ''
        num = pat.SINGULAR if not data.get('aplural') or data.get('agent') not in ('me', 'you') else pat.PLURAL
      
        #aux.append(aux[0])
        verbaspect = None
        for (ll, l, c, n) in zip(aux_doc,aux_doc[1:],aux_doc[2:],aux_doc[3:]): #ll = last last, l = last, c = current, n = next
            if c.lemma_ == '.':
                continue

            if c.lemma_ == 'not':
                if l.lemma_ == 'be':
                    if n.lemma_ == 'be':
                        
                        verbtense = pat.tenses(c.text)[0][0]
                        final_aux += pat.conjugate('be',tense=pat.tenses(l.text)[0][0],number=num) + ' '
                        verbaspect = pat.PROGRESSIVE
                    else:
                        final_aux += pat.conjugate('do',tense=pat.tenses(l.text)[0][0],number=num) + ' '
                        verbtense = pat.INFINITIVE
                final_aux += 'not '
            elif c.lemma_ == 'be':
                if l.lemma_ == 'be':
                    print("progressive")
                    verbtense = pat.tenses(c.text)[0][0]
                    final_aux += pat.conjugate('be',tense=pat.tenses(c.text)[0][0],number=num) + ' '
                    verbaspect = pat.PROGRESSIVE
                elif l.tag_ == 'MD':
                    verbtense = pat.INFINITIVE
            elif c.lemma_ == 'have':
                num == pat.PLURAL if l.tag_ == 'MD' else num
                final_aux += pat.conjugate('have',tense=pat.tenses(c.text)[0][0],number=num) + ' '
                    #verbtense = pat.tenses(n.text)[0][0]
            elif c.tag_ == 'MD':
                num == pat.PLURAL
                final_aux += pat.conjugate(c.lemma_,tense=pat.tenses(n.text)[0][0],number=num) + ' '
                    #verbtense = pat.tenses(n.text)[0][0]
            else:
                final_aux += c.text_with_ws
        final_aux = final_aux.lower().strip()    

         # conjugate main verb:
        print("number")
        print(num)
        if verbaspect:
            verbActive = pat.conjugate(verbLemma,tense=tense,aspect=verbaspect, number=num)
        else:
            verbActive = pat.conjugate(verbLemma,tense=tense, number=num)

        if final_aux is not None and verbActive is not None:
            finalVerb = final_aux + " " + verbActive
            print("finalVerb")
        else:
            print("One is NONE")
            print("final_aux")
            print(final_aux)
            print("verbActive")
            print(verbActive)
        return finalVerb


    
"""print("tense")
print(tense)
verbActive = pat.conjugate(verbLemma, tense, , number)
print("Verb Active: ")
print(verbActive)"""