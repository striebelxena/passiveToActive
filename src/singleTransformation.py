import passiveToActive
import evaluation.singleEvaluation as ev
source ='singleTransformation'

continueProgramm='y'

while (continueProgramm =='y'):
    sentence=input('\n\nPassive sentence:\n\n')

    transformedSentence = passiveToActive.passiveToActive(sentence, source)

    evaluation= input('\n\nEvaluate Sentence? (y/n)\n\n')

    if(evaluation=='y'):
        goldstandard= input('\n\nEnter your expected active sentence:\n\n')
        ev.evaluate_sentence_results (goldstandard, transformedSentence)

    else:
        continueProgramm=input('\n\nContinue Programm? (y/n)\n\n')
        if(continueProgramm=='n'):
            print('Programm finished')
            break
        else: continue



