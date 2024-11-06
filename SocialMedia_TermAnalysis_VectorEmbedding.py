# -*- coding: utf-8 -*-
"""SocialMedia_TermAnalysis_VectorEmbedding.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nl8NRNDU8bNZwjVRrZspCaHy33qk_VKt

#**Sparse Vector (Embedding)**

**1. Importing Required Libraries**

We start by importing essential Python libraries for data manipulation, visualization, and NLP.
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import nltk
from wordcloud import WordCloud
import spacy

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

"""**2. Load and Explore the Dataset**

We load the dataset and check its structure to understand the data we are working with.
"""

# Load the dataset (replace 'social_media_data.csv' with your actual file path)
df = pd.read_csv('/content/synthetic_social_media_data.csv')

# Display the first few rows of the dataset
print(df.head())

# Check the column names and data types
print(df.info())

# Check for any missing values
print(df.isnull().sum())

"""**3. Data Preprocessing**

Since the dataset includes a "Post Content" column, we preprocess the text by converting it to lowercase, removing punctuation, and cleaning it for further analysis.
"""

# Basic Text Cleaning: Lowercase conversion, removing punctuation, and handling missing values
df['Post Content'] = df['Post Content'].fillna('').str.lower()
df['Post Content'] = df['Post Content'].str.replace('[^a-z\s]', '', regex=True)

# Display a sample of the cleaned text
print(df['Post Content'].head())

"""**4. TF-IDF Calculation**

Here, we compute the Term Frequency-Inverse Document Frequency (TF-IDF) for specific words like "car", "auto", "insurance", and "best" in the "Post Content" column.
"""

# Define the query terms for TF-IDF
query_terms = ['car', 'auto', 'insurance', 'best']

# Initialize the TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(vocabulary=query_terms)

# Compute the TF-IDF matrix for 'Post Content'
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Post Content'])

# Convert the TF-IDF matrix to a DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=query_terms)

# Display the TF-IDF weights
print("TF-IDF Weights for Terms:")
print(tfidf_df.head())

"""**5. Euclidean Normalization**

After calculating the term frequencies, we normalize the values using Euclidean normalization to standardize the term frequencies.
"""

# Apply Euclidean normalization to the TF-IDF values
tfidf_normalized = normalize(tfidf_df, norm='l2', axis=1)

# Convert normalized values back to DataFrame
tfidf_normalized_df = pd.DataFrame(tfidf_normalized, columns=query_terms)

# Display normalized TF-IDF weights
print("Normalized TF-IDF Weights:")
print(tfidf_normalized_df.head())

"""**6. Cosine Similarity**

We now compute the Cosine Similarity between different documents to identify the similarity between the terms.


"""

# Compute Cosine Similarity between the terms in the TF-IDF matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Create dynamic labels for each document
doc_labels = [f'Doc{i+1}' for i in range(tfidf_matrix.shape[0])]

# Convert the cosine similarity matrix to DataFrame for all documents
cosine_sim_df = pd.DataFrame(cosine_sim, columns=doc_labels, index=doc_labels)

# Display the cosine similarity matrix
print(cosine_sim_df.head())

"""**7. Word Embeddings Using SpaCy**

To generate a word embedding for each term, we use SpaCy, a popular NLP library. Word embeddings capture the semantic similarity between words.


"""

# Example words to create embeddings for: 'car', 'auto', 'insurance', 'best'
words = ['car', 'auto', 'insurance', 'best']

# Create word embeddings using SpaCy
word_embeddings = {word: nlp(word).vector for word in words}

# Display the word embeddings
for word, vector in word_embeddings.items():
    print(f"Word: {word}, Embedding Vector: {vector[:10]}...")  # Print only first 10 dimensions

"""**8. Plotting Word Embeddings**

We plot the word embeddings to visually understand the relationship between terms like "car" and "auto" (which are semantically similar).
"""

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reduce the dimensions of the word embeddings for 2D plotting
pca = PCA(n_components=2)
word_vectors = np.array([vector for vector in word_embeddings.values()])
word_vectors_2d = pca.fit_transform(word_vectors)

# Plot the word embeddings
plt.figure(figsize=(8, 6))
plt.scatter(word_vectors_2d[:, 0], word_vectors_2d[:, 1], color='blue')

# Annotate the plot with words
for i, word in enumerate(words):
    plt.annotate(word, xy=(word_vectors_2d[i, 0], word_vectors_2d[i, 1]))

plt.title('2D Plot of Word Embeddings')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()

"""**9. Finding Nearest Neighbors Using Cosine Similarity**

Now we calculate the nearest neighbors of a word based on cosine similarity, showing how close words like "car" and "auto" are in the vector space.
"""

# Function to find the nearest word using cosine similarity
def nearest_word(word, word_embeddings):
    word_vec = word_embeddings[word]
    nearest = None
    max_similarity = -1

    # Compare with every other word
    for other_word, other_vec in word_embeddings.items():
        if word != other_word:
            # Calculate cosine similarity
            similarity = cosine_similarity([word_vec], [other_vec])[0][0]
            if similarity > max_similarity:
                max_similarity = similarity
                nearest = other_word
    return nearest, max_similarity

# Example word list
words = ['car', 'auto', 'insurance', 'best']

# Create word embeddings using SpaCy
word_embeddings = {word: nlp(word).vector for word in words}

# Find the nearest word to 'car'
nearest, similarity = nearest_word('car', word_embeddings)

# Print the result
print(f"The nearest word to 'car' is '{nearest}' with cosine similarity {similarity:.4f}")

"""**10. Pointwise Mutual Information (PMI)**

We use PMI to measure how often words co-occur in a dataset, especially when low-frequency words appear together.
"""

from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

# Tokenize the 'Post Content' for PMI calculations
tokens = [nltk.word_tokenize(content) for content in df['Post Content']]
tokens_flat = [token for sublist in tokens for token in sublist]

# Compute PMI for word pairs using NLTK's BigramCollocationFinder
bigram_measures = BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens_flat)

# Find top word pairs based on PMI
pmi_bigrams = finder.nbest(bigram_measures.pmi, 10)
print("Top 10 Word Pairs by PMI:")
print(pmi_bigrams)

"""### **Conclusion**
This code performs several tasks, including:
1. **TF-IDF** calculation to compute term importance.
2. **Cosine Similarity** to measure similarity between terms and documents.
3. **Word Embeddings** to capture semantic meaning in the vector space.
4. **Nearest Neighbors** to find similar words using cosine similarity.
5. **PMI** to analyze word co-occurrence.

This approach provides insights into how social media content can be analyzed to uncover patterns, similarities, and relationships between key terms.
"""