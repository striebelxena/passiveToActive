# passiveToActive-with-NLP

This is a ruled-based approach to convert regulatory passive sentences to active sentences. The data pipeline uses SpaCy to perform NLP tasks like tokenization, POS Tagging, Dependency Parsing. The result is checked for passive constructions and then based on the morphological and syntax characteristics the transformation from passive to active is performed. Finally, the converted sentence is returned. If there is no agent provided, the algorithm uses "one" as default subject for the active sentence.

Author: Xena Striebel

Course: Master Praktikum, Approaching Informations Systems Challenges with NLP

Instructor: Catherine Sai

---

## **Installation**

For installing and running this project please use conda and proceed like this:

Clone the repository:

```
git clone https://github.com/striebelxena/passiveToActive.git
```

Navigate to the project directory:

```
cd passiveToActive
```

Create a new Conda environment:

```
conda create --name pta python=3.11
```

Activate the Conda environment:

```
conda activate pta
```

Install pattern:

```
conda install -c conda-forge pattern
```

Install required packages and language model:

```
pip install -r requirements.txt
python -m spacy download en_core_web_lg 
```



To being able to run the algorithm navigate to the source folder:

```
cd src
```

To finally run the algorithm for one sentence use this command and follow the instructions:

```
python singleTransformation.py
```

To finally run the algorithm for a xlsx-file of sentences use this command and follow the instruction:

```
python fileTransformation.py
```
When the algorithm executed for the first time, it might take some time to load everything.

Implementation Pipeline:
------------------------

If the input sentence has one passive construction, the algorithm has the following basic pipeline:

1. Input sentence
2. Perform NLP tasks like tokenization, POS tagging, dependency parsing, named entity recognition on input sentence
3. Check for passive voice
4. Split sentence into preclause, passive construction, postclause
5. Analyse POS-Tags and dependencies of every word in passive construction
6. Conjugate verb
7. Invert subject and object as required
8. Compose new active constructions based on identified components and active verb
9. Assemble preclause + active construction + postclause
10. Return final active sentence

---

Usage:
------

There are two options how the algorithm can be used:

1. **Transformation of only one sentence:**
   1. Run singleTransformation.py (Starting the code usually takes some time)
   2. Insert one sentence via the terminal
   3. Output: transformed sentence
   4. State whether you want to compare the output to a expected result
   5. If yes, insert your reference sentence
2. **Transformation of several sentences at once:**
   1. Prepare a xlsx-file with the following characteristics:
      * One column called “InputSentence” with the sentences which should be converted, one in each row
      * If the output should be evaluated based on the ability of the algorithm to identify passive sentences and to transform them, the file needs a column called
        * "ReferenceSentence", which
          inherits the expected output, i.e. the active sentence and another column called
        * "Mode", which inherits whether the InputSentence is indeed passive or active
   2. Run fileTransformation.py
   3. Insert the location where the input file is located
   4. Insert the location where you want the output file to be saved
   5. State whether you want to evaluate the output
   6. Output: The transformed sentences and, if evaluated, their semantic similarity score is saved to a new xlsx.file, which you specified ealier

## Assumptions:

The whole data pipeline depends on the accuracy and correctness of the parser.

## Evaluation:

The algorithm is evaluated by considering both the ability to identify
passive constructions in inserted sentences as well as the correctness of the
passive-to-active conversion. The evaluation of the transformed sentences is done by comparing the semantic similarity of the generated output sentences with the expected one by applying the SBERT function. Herein, the cosine semantic similarity is calculated and returned.

Overall, precision and recall were defined and used as following:

**True Positive (TP):** correctly identified as passive and
transformed correctly (SBERT-Score > 0.95)

**False Positive (FP):** wrongly identified as passive and
attempted to transform

**True Negative (TN):** correctly identified as active and thus not
transformed

**False Negative (FN):** (wrongly identified as active and
not transformed) PLUS (correctly identified as passive and transformed wrongly
(SBERT-Score <= 0.95)

Evaluating the algorithm with the file called "Goldstandard_updated.xlsx, the following results were generated:

| **TP:**        | 150    |
| :------------------- | :----- |
| **FP:**        | 0      |
| **TN:**        | 15     |
| **FN:**        | 10     |
| **Precision:** | 1      |
| **Recall:**    | 0.9375 |

Also an human evaluation was done, which resulted in an accuracy of 93.75%.

## Limitations & Outlook:

**Limitations of the Algorithm:**

* Struggles sometimes with sentences containing multiple passive constructions, leading to complexity in parsing and handling components.
* Difficulty in correctly transforming complex or rare sentence constructions.
* Issues with SpaCy's dependency parsing.
* SBERT-Score inconsistencies, even with grammatically and semantically correct transformations, due to word order differences or parsing ambiguities.
* Parsing issues with symbolics or punctuation using SpaCy.

**Further Improvements:**

* Potential enhancements include using CFG or constituency parsing for better analysis, integrating tools for spelling and grammar correction, and employing machine learning models for improved punctuation and sentence composition.
* Exploring the use of alternative NLP tools like Stanford Parser or NLTK for more precise parsing.
* The possibility of deriving the agent from context rather than defaulting to "one".
* The approach is pioneering in transforming complex, long, regulatory sentences with a rule-based algorithm.

Project Organization
--------------------

    ├── LICENSE
    ├── README.md          <- The top-level README for all instructions and information
    │
    ├── documents              <- Folder with report, presentation, final human evaluation
    │
    │
    ├── requirements.txt   <- The requirements file
    │
    │
    ├── src                <- Source code for to use in this project.
    │   │
    │   ├── analysePassiveConstruction    <- function that parses and analyses the identified passive construction
    │   │
    │   ├──archive  <- old files, in which other approaches were tried, however code might be not executable
    │   │  
    │   ├── checkForPassive         <- Folder with the function to check and identify passive constructions
    │   ├── composition               <- Folder with the function to compose the active sentence
    │   ├── evaluation                   <- Folder with the function to evaluate the output sentence
    │   ├── verbConjugation         <- Folder with the function to conjugate the active verb
    │   ├── fileTransformation       <- Script to transform many sentences at once with an xlsx-file as input
    │   ├── passiveToActive           <- Main function for transformation
    │   └── singleTransformation   <- Script to transform one single sentence

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
