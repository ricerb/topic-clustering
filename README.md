# Topic clustering exploration

Run the notebooks in the following order:

1. stem and tokenize.ipynb
    - This script preprocesses an input table of text (titles, absracts, or anything else).

2. TFIDF encoding and NMF clustering.ipynb
    - This is where the unsupervised clustering happens...
    - Tokenized text data is fed into NMF model, then prepared for visualization using TSNE.

3. Visualization.ipynb
    - 2D or 3D plotly visualizations provided.

## Setup

To setup the environment:

```bash
git clone git@github.com:ricerb/topic-clustering.git
cd topic-clustering

# create new virtual environment
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

To run from the command line:

```bash
# view help
refml --help

# run something
refml do-it
```


