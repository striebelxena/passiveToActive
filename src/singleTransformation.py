import passiveToActive as passiveToActive
import evaluation.evaluation as ev

source = "singleTransformation"
continueProgramm = "y"
semantic_similarity = 0
dependency_similarity = 0

while continueProgramm == "y":
    # Insert your passive sentence here
    sentence = input("\n\nPassive sentence:\n\n")

    if not sentence:
        print("No sentence entered")
        continue

    try:
        # Sentence transformation
        transformedSentence, transformedSubclauses = passiveToActive.passiveToActive(
            sentence, source
        )
        # Input with no passive construction identified
        if transformedSentence == "No passive construction identified":
            print(transformedSentence)
            continue
        # Input with no sentence in English
        elif transformedSentence == "Sentence is not in English":
            print(f"{transformedSentence}, please enter a sentence in English")
            continue

        # Evaluation: compare output with expected active sentence
        evaluation = input("\n\nEvaluate Sentence? (y/n)\n\n")

        if evaluation == "y":
            semantic_similarity = 0
            # Insert your expected active sentence here

            goldstandard = input("\n\nEnter your expected active sentence:\n\n")
            goldstandard = " ".join(goldstandard.split())
            # Calculate the semantic similarity score between output and goldstandard with SBERT for every transformed subclause and then calculate the average
            for key, subclause in transformedSubclauses.items():
                semantic_similarity = (
                    semantic_similarity
                    + ev.evaluate_sentence_results(
                        goldstandard, transformedSentence, subclause, source
                    )
                )

                final_semantic_similarity = semantic_similarity / len(
                    transformedSubclauses
                )
            print(f"\nSemantic Similarity: {final_semantic_similarity}")

        else:
            continueProgramm = input("\n\nContinue Programm? (y/n)\n\n")
            if continueProgramm == "n":
                print("Programm finished")
                break
            else:
                continue
    except Exception as e:
        print(f"An unexpected error occured: {e}")
