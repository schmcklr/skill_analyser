# import necessary libraries
import pandas as pd
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# download NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')

# create a list of texts
texts = ["this is a text about topic1", "this is a text about topic2", "this is a text about topic3"]


# Create a example DataFrame
df = pd.DataFrame({'text': ["this is a text about topic1", "this is a text about topic2", "this is a text about topic3"]})

# function to preprocess the texts
def preprocess_texts(texts):
    # create a list to store the preprocessed texts
    preprocessed_texts = []
    # get english stopwords
    stop_words = set(stopwords.words('english'))
    # for each text
    for text in texts:
        # tokenize the text
        words = word_tokenize(text)
        # remove stopwords and lowercase the remaining words
        words = [word.lower() for word in words if word.isalpha() and word not in stop_words]
        # add the preprocessed text to the list
        preprocessed_texts.append(words)
    # return the list of preprocessed texts
    return preprocessed_texts

# preprocess the texts
texts = preprocess_texts(df["text"])

# create a dictionary
dictionary = corpora.Dictionary(texts)

# create a corpus
corpus = [dictionary.doc2bow(text) for text in texts]

# create an LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=3, id2word=dictionary)

# print the topics
print(lda_model.print_topics())

