from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


# Latent Semantic Analysis (LSA):
def analysis_with_lsa (df, year, column, topics):
    print('\n2. Latent Semantic Analysis (LSA):')
    # create a Tf-idf vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # fit the vectorizer on the text data
    X = vectorizer.fit_transform(df[year][column])

    # perform SVD on the Tf-idf matrix
    svd = TruncatedSVD(n_components=topics)

    # extract the top words for each topic
    top_words = vectorizer.get_feature_names_out()

    # print the top words for each topic
    n_top_words = 15
    for topic_idx, topic in enumerate(svd.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([top_words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))