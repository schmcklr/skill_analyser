# Latent Dirichlet Allocation (LDA):
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer


def analysis_with_lda (df, year, column, topics):
    print('\n1. Latent Dirichlet Allocation (LDA):')

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(max_df=1, min_df=1, stop_words='english')
    X = vectorizer.fit_transform(df[year][column])

    # performing topic modeling using LDA
    lda = LatentDirichletAllocation(n_components=topics, max_iter=10, learning_method='batch', random_state=0)
    lda.fit(X)

    # output of topics and words for LDA
    n_top_words = 15
    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))