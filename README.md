# Topic clustering exploration

Run the notebooks in the following order:

1. stem and tokenize.ipynb
    - This script preprocesses an input table of text (titles, absracts, or anything else).

2. TFIDF encoding and NMF clustering.ipynb
    - This is where the unsupervised clustering happens...
    - Tokenized text data is fed into NMF model, then prepared for visualization using TSNE.

3. Visualization.ipynb
    - 2D or 3D plotly visualizations provided.