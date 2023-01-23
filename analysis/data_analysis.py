# Preprocessing, used to clean uo the job description
import pandas as pd
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from preprocessing.data_preprocessing import job_data, composite_skills

# display options for dataframes
from visualization.data_visualization import visualization

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)


# Define a function to keep only nouns and remove other word groups
#df['tagged_text'] = df['qualifications'].apply(lambda x: nltk.pos_tag(nltk.word_tokenize(x)))
#df['qualifications'] = df['tagged_text'].apply(lambda x: ' '.join([word for word, pos in x if pos.startswith('N')]))


# selecting nouns and converting to a string
#job_data["qualifications"] = job_data["qualifications"].apply(lambda x: ' '.join([token for token, tag in nltk.pos_tag(x) if tag.startswith('NN')]))


# initialize lemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatize_text(text):
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

def lemmatize_text(word):
    if word in composite_skills:
        return word
    else:
        return lemmatizer.lemmatize(word)



# performing lemmatization for dataset
#job_data['descriptionLemmatized'] = job_data['descriptionTokenized'].apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))
job_data['descriptionLemmatized'] = job_data['descriptionTokenized'].apply(lambda x: " ".join([lemmatize_text(word) for word in x.split()]))

job_data.to_excel('jobData.xlsx', index=False)

# group the DataFrame by year
grouped = job_data.groupby(job_data['created_at'].dt.year)

# create a dictionary to store the new DataFrames
year_dfs = {}

# split the groups into separate DataFrames and store them in the dictionary
for year, group in grouped:
    year_dfs[year] = group.copy()

for year in year_dfs:
    print(year)
    print(year_dfs[year])


    # defining the number of topics
    n_topics = 2
    # 1. Latent Dirichlet Allocation (LDA):
    print('\n1. Latent Dirichlet Allocation (LDA):')

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(max_df=1, min_df=1, stop_words='english')
    X = vectorizer.fit_transform(year_dfs[year]['descriptionLemmatized'])

    # performing topic modeling using LDA
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=10, learning_method='batch', random_state=0)
    lda.fit(X)

    # output of topics and words for LDA
    n_top_words = 15
    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

    #################################TEST############################################
    n_topics = 5

    # 2. Latent Semantic Analysis (LSA):
    print('\n2. Latent Semantic Analysis (LSA):')
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Create a Tf-idf vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit the vectorizer on the text data
    X = vectorizer.fit_transform(year_dfs[year])

    # Perform SVD on the Tf-idf matrix
    svd = TruncatedSVD(n_components=n_topics)
    X_reduced = svd.fit_transform(X)

    # Extract the top words for each topic
    top_words = vectorizer.get_feature_names_out()

    # Print the top words for each topic
    for topic_idx, topic in enumerate(svd.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([top_words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

    # 3. Non-Negative Matrix Factorization (NMF):
    print('\n3. Non-Negative Matrix Factorization (NMF):')
    from sklearn.decomposition import NMF
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Create a Tf-idf vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit the vectorizer on the text data
    X = vectorizer.fit_transform(job_data['descriptionLemmatized'])

    # Perform NMF on the Tf-idf matrix
    nmf = NMF(n_components=n_topics)
    X_reduced = nmf.fit_transform(X)

    # Extract the top words for each topic
    top_words = vectorizer.get_feature_names_out()

    # Print the top words for each topic
    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([top_words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

    # 3. Token frequencies:
    print('\n3. Token frequencies:')
    # initialize countVectorizer
    vectorizer2 = CountVectorizer()

    # convert the text data into a matrix of token frequencies
    X = vectorizer2.fit_transform(year_dfs[year]['descriptionLemmatized'])

    # Berechnen der Token-Häufigkeiten
    token_counts = X.sum(axis=0).A1

    # Die 10 häufigsten Token ausgeben
    most_common_tokens = [vectorizer2.get_feature_names_out()[i] for i in token_counts.argsort()[-500:]]
    print(most_common_tokens)

    # visualization
    #data_string = ' '.join(year_dfs[year]['descriptionLemmatized'].tolist())
    #print(year_dfs[year]['descriptionLemmatized'])
    #print(data_string)
    #visualization(year, year_dfs[year]['descriptionLemmatized'].to_string())




    # Obtain the token counts in the form of a sparse matrix
    token_counts2 = X.toarray()

    # Extract the vocabulary of tokens
    vocab = vectorizer2.get_feature_names_out()

    # Create a dictionary to store the token counts
    token_counts_dict = dict(zip(vocab, token_counts2.sum(axis=0)))

    print(token_counts_dict)

    visualization(year, token_counts_dict)


