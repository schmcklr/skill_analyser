## Visualize data
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def visualization(vectorizer, X, year):

    # obtain the token counts in the form of a sparse matrix
    token_counts2 = X.toarray()

    # extract the vocabulary of tokens
    vocab = vectorizer.get_feature_names_out()

    # create a dictionary to store the token counts
    token_counts_dict = dict(zip(vocab, token_counts2.sum(axis=0)))

    # Create and generate a word cloud image:
    plt.suptitle(year, fontsize=24, fontweight='bold')
    wordcloud = WordCloud().generate_from_frequencies(token_counts_dict)
    print("\n***",year,"***\n")
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()