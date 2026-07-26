from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfSearch:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(documents)

    def search(self, query, top_k=5):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.doc_vectors)[0]
        top_indices = scores.argsort()[-top_k:][::-1]
        return top_indices, scores[top_indices]