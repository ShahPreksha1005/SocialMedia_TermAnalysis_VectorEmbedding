# SocialMedia_TermAnalysis_VectorEmbedding

## Project Overview
This project analyzes social media posts by computing vector embeddings and other metrics to understand relationships and patterns among key terms. Using methods like TF-IDF, Cosine Similarity, and Pointwise Mutual Information (PMI), we identify semantic similarities and co-occurrences in terms such as "car," "auto," and "insurance." These analyses can offer insights into content patterns, term importance, and term similarity.

## Key Techniques
- **TF-IDF Calculation**: Measures term importance in the "Post Content" column for words like "car," "insurance," and "best."
- **Cosine Similarity**: Computes the similarity between different terms to identify closely related terms.
- **Word Embeddings**: Uses SpaCy to generate word embeddings, capturing semantic similarity in vector space.
- **Euclidean Normalization**: Normalizes term frequencies for standardization.
- **Pointwise Mutual Information (PMI)**: Analyzes word co-occurrence frequency, especially among low-frequency terms.
- **Nearest Neighbors**: Identifies words that are closest in meaning based on cosine similarity.

## Conclusion
This project illustrates how text data from social media posts can be analyzed to reveal meaningful relationships between terms. These techniques allow for deeper insights into term importance, semantic relationships, and patterns within social media content. Such analyses are valuable for applications in sentiment analysis, content recommendation, and social media trend analysis.

## Requirements
- Python 3.x
- Pandas, Matplotlib, Seaborn, SpaCy

---
