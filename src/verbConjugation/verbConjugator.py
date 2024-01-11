import pattern_patch 
import pattern.text.en as pat
import spacy
nlp = spacy.load("en_core_web_lg", exclude = ['morphologizer','ner'])
#thirdPerson = pat.conjugate('have',tense='present',person=3, number=pat.SINGULAR) 
#print(thirdPerson)

#  verb conjugation
def conjugateVerb(data):
        verbLemma = data.get('verbLemma')
        tense = data.get('verbTense')
        aux = list(data.get('aux'))
        verbAspect = data.get('verbAspect')
        aux_doc = nlp(' '.join(aux))
        finalVerb = {'auxilaryVerb':'', 'activeVerb':''}
       

        finalAux = []
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
           print("finalaux")
           print(finalAux)

           if c.lemma_ == '.':
                continue

           if  n.lemma_ == 'not':
                print("n.lemma")
                print(n.lemma_)
                if l.lemma_ == 'be':
                    if n.text == 'being':
                        finalAux.append(pat.conjugate('be',tense=pat.tenses(l.text)[0][0],number=num))
                        verbAspect = pat.PROGRESSIVE
                    else:
                        finalAux.append(pat.conjugate('do',tense=pat.tenses(l.text)[0][0],number=num))
                        
                elif l.lemma_ == 'have':
                    finalAux.append(pat.conjugate('have',tense=pat.tenses(l.text)[0][0],number=num))
                      
                elif c.lemma_ == 'have':
                    num = pat.PLURAL if l.tag_ == 'MD' else num
                    if num == 'singular':
                        print("third person")
                        print(pat.tenses(c.text)[0][0])
                        if pat.tenses(c.text)[0][0] == 'infinitive':
                            finalAux.append(pat.conjugate('have',tense='present',person=3, number=num))
                        else:
                            finalAux.append(pat.conjugate('have',tense=pat.tenses(c.text)[0][0],person=3, number=num))
                    else:
                        finalAux.append(pat.conjugate('have',tense=pat.tenses(c.text)[0][0],number=num))
                elif c.tag_ == 'MD' or c.lemma_ == 'will':
                    num = pat.PLURAL
                    finalAux.append(pat.conjugate(c.lemma_,tense=pat.tenses(n.text)[0][0],number=num)) 
                    
                
                finalAux.append('not')
                
           elif c.lemma_ == 'be':
                if n.text == 'being':
                    print("progressive")
                    finalAux.append(pat.conjugate('be',tense=pat.tenses(c.text)[0][0],number=num))
                    verbAspect = pat.PROGRESSIVE
               
           elif c.lemma_ == 'have':
                num = pat.PLURAL if l.tag_ == 'MD' else num
                if num == 'singular':
                    print("third person")
                    print(pat.tenses(c.text)[0][0])
                    if pat.tenses(c.text)[0][0] == 'infinitive':
                        finalAux.append(pat.conjugate('have',tense='present',person=3, number=num))
                    else:
                        finalAux.append(pat.conjugate('have',tense=pat.tenses(c.text)[0][0],person=3, number=num))
                else:
                    finalAux.append(pat.conjugate('have',tense=pat.tenses(c.text)[0][0],number=num))
           elif c.tag_ == 'MD' or c.lemma_ == 'will':
                num = pat.PLURAL
                finalAux.append(pat.conjugate(c.lemma_,tense=pat.tenses(n.text)[0][0],number=num))
           else:
                if c.lemma_ != 'not':
                    finalAux.append(c.text)

        print("final Aux vor neg")
        print(finalAux)
        modal_aux_verbs = ['should', 'would', 'could', 'have', 'shall', 'will', 'may', 'might', 'must']
        
        for index, element in enumerate(finalAux):
            if any(element in modal_aux_verbs for element in finalAux):
                break
            elif element == "not" and num == pat.SINGULAR:
                finalAux[index] = "does not"
                num = pat.PLURAL
            elif element == "not" and num == pat.PLURAL:
                finalAux[index]= "do not"
            
        finalAux = ' '.join(finalAux)
        finalAux.lower().strip()
        print("finalAux")
        print(finalAux)
         # conjugate main verb:
        print("Num: " + str(num))
        if verbAspect:
            verbActive = pat.conjugate(verbLemma,tense=tense,aspect=verbAspect, number=num)
        else:
            verbActive = pat.conjugate(verbLemma,tense=tense, number=num)

        if finalAux is not None and verbActive is not None:
            finalVerb['auxilaryVerb'] = finalAux
            finalVerb['activeVerb'] = verbActive
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
        
        return finalVerb


    