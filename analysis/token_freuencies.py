from sklearn.feature_extraction.text import CountVectorizer


# 3. Token frequencies:
def get_token_frequencies (vectorizer, X):
    print('\n3. Token frequencies:')

    # calculate the token frequencies
    token_counts = X.sum(axis=0).A1

    # get most common tokens
    most_common_tokens = [vectorizer.get_feature_names_out()[i] for i in token_counts.argsort()[-100:]]
    print(most_common_tokens)

