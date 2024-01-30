import passiveToActive as passiveToActive
import evaluation.evaluation as ev
import questionary
from rich.console import Console
from rich import print as rprint

source = "singleTransformation"
console = Console()
continueProgramm = True
semantic_similarity = 0
dependency_similarity = 0

while continueProgramm:
    # Insert your passive sentence here
    sentence = questionary.text(
        "\n\nPlease enter a passive sentence or enter c to stop the program:\n"
    ).ask()
    if sentence == "c":
        continueProgramm = False
        rprint("[bold white]Program finished[/bold white]")
        break
    if not sentence:
        rprint("[yellow]No sentence entered[/yellow]")
        continue

    try:
        # Sentence transformation
        transformedSentence, transformedSubclauses = passiveToActive.passiveToActive(
            sentence, source
        )
        # Input with no passive construction identified
        if transformedSentence == "\nNo passive construction identified":
            rprint(f"[red]{transformedSentence}[/red]")
            continue
        elif transformedSentence == "Sentence is not in English":
            rprint("[yellow]Please enter a sentence in English[/yellow]")
            continue

        # Evaluation: compare output with expected active sentence
        evaluation = questionary.confirm("\nEvaluate Sentence?").ask()

        if evaluation:
            semantic_similarity = 0
            # Insert your expected active sentence here

            goldstandard = questionary.text(
                "\nEnter your expected active sentence:"
            ).ask()
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
            rprint(
                f"\n[green]Semantic Similarity: {final_semantic_similarity:.2f}[/green]"
            )

        else:
            continueProgramm = questionary.confirm("\nContinue Program?").ask()
            if not continueProgramm:
                rprint("[bold white]Program finished[/bold white]")
                break
            else:
                continue
    except Exception as e:
        rprint(f"[bold red]An unexpected error occurred: {e}[/bold red]")
