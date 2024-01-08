import passiveToActive
import evaluation.singleEvaluation as ev
source ='singleTransformation'

sentence=input('\n\nPassive sentence:\n\n')

transformedSentence = passiveToActive.passiveToActive(sentence, source)

evaluation= input('\n\nEvaluate Sentence? (y/n)\n\n')

if(evaluation=='y'):
    goldstandard= input('\n\nEnter your expected active sentence:\n\n')
    ev.evaluate_sentence_results (goldstandard, transformedSentence)

else:
    print('Programm finished')



