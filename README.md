passiveToActive-with-NLP
========================

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

Install required packages:

```
pip install -r requirements.txt
```

If there occurs an error during the installation of pattern, please try this command:

```
conda install -c conda-forge pattern.
```

To being able to run the algorithm navigate to the source folder:

```
cd src
```

To finally run the algorithm for one sentence use this command:

```
python singleTransformation.py
```

To finally run the algorithm for a xlsx-file of sentences use this command:

```
python fileTransformation.py
```

git clone https://github.com/striebelxena/passiveToActive.git
cd passiveToActive
conda create --name pta python=3.11
conda activate pta

pip install spacy
pip install pattern
python -m spacy download en_core_web_lg
pip install langdetect
pip install pandas
pip install openpyxl

pip install -r requirements.txt

cd scr
 conda install -c conda-forge pattern.

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
   1. Prepare a csv-file with the following characteristics:
      * One column called “InputSentence” with
        the sentences which should be converted, one in each row
      * The csv-file as to be located in the“data”
        folder, otherwise the directory has to be changed accordingly
      * If the output should be evaluated based on the ability of the algorithm to identify passive sentences and to transform them, the cvs-file needs a column called

        * "ReferenceSentence", which
          inherits the expected output, i.e. the active sentence and another column called
        * "Mode", which inherits whether the InputSentence is indeed passive or active
   2. Run fileTransformation.py
   3. State whether you want to evaluate the output
   4. Output: The transformed sentences and, if evaluated, their semantic similarity score is saved to an new csv-file which per default will be created in the folder "data"

# Assumptions:

The whole data pipeline depends on the accuracy and correctness of the parser.

# Evaluation:

The evaluation of the transformed sentences is done by comparing the semantic similarity of the generated output sentences with the expected one by applying the SBERT function. Herein, the cosine semantic similarity is calculated and returned.

# Limitations & Outlook:

Project Organization
--------------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like`make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
