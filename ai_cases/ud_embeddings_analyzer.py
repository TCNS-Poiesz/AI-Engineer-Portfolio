import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

class UDEmbeddingsAnalyzer:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        self.matrix = None
        self.df = None

    def load(self, csv_path):
        self.df = pd.read_csv(csv_path)
        return self.df

    def fit(self):
        texts = self.df["free_text"].fillna("").tolist()
        self.matrix = self.vectorizer.fit_transform(texts)
        self.df["cluster"] = self.kmeans.fit_predict(self.matrix)
        return self.df

    def search(self, query, top_k=5):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).flatten()
        top_idx = sims.argsort()[::-1][:top_k]
        return self.df.iloc[top_idx].assign(similarity=sims[top_idx])

    def cluster_playbooks(self):
        # Most common resolution per cluster
        playbooks = (
            self.df.dropna(subset=["resolution"])
            .groupby("cluster")["resolution"]
            .agg(lambda x: x.value_counts().index[0])
            .reset_index()
        )
        return playbooks
