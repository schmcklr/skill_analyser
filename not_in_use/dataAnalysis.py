# Preprocessing, used to clean uo the job description
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from not_in_use.dataPreprocessing import preprocessedJobData

# display options for dataframes
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

# load dataframe from dataImport
df = preprocessedJobData

# Convert text to lowercase
df['qualifications'] = df['qualifications'].str.lower()

# Remove stopwords
stopEnglish = stopwords.words('english')
df['qualifications'] = df['qualifications'].apply(lambda x: " ".join(x for x in x.split() if x not in stopEnglish))
# TODO: isn't necessary anymore because all german words were translated (en) -> clean
# stopGerman = stopwords.words('german')
#df['qualifications'] = df['qualifications'].apply(lambda x: " ".join(x for x in x.split() if x not in stopGerman))

# Remove punctuation
df['qualifications'] = df['qualifications'].str.replace('[^\w\s]','', regex=True)

# tokenize
df["qualifications"] = df["qualifications"].apply(nltk.word_tokenize)

print('Tokens')
print(df["qualifications"])

# translate
df2 = df.iloc[:2]
from googletrans import Translator
from langdetect import detect
translator = Translator()

print(df2)
#df2["qualifications"] = df2["qualifications"].apply(translator.translate, src='de', dest='en').apply(getattr, args=("text",))
#df2["qualifications"] = df2["qualifications"].apply(lambda x: translator.translate(x, src='de', dest='en') if translator.translate(x, src='de', dest='en') else x)


print('Translation of job advertisements...')
translated_job_ads = 0
all_job_adds = 0
for index, row in df.iterrows():
    translated_list = []
    all_job_adds += 1
    if detect(row["description"]) == 'de':
        translated_job_ads += 1
        for element in row["qualifications"]:
            translated = translator.translate(element, src='de', dest='en').text
            # TODO: remove debugging function
            #print(element + '->' + translated)
            translated_list.append(translated)
    else:
        for element in row["qualifications"]:
            translated_list.append(element)
    row["qualifications"] = translated_list

print('Translation successful! ' + str(translated_job_ads) + '/' + str(all_job_adds) + ' job advertisements were translated')

print(df2)


# Define a function to keep only nouns and remove other word groups
#df['tagged_text'] = df['qualifications'].apply(lambda x: nltk.pos_tag(nltk.word_tokenize(x)))
#df['qualifications'] = df['tagged_text'].apply(lambda x: ' '.join([word for word, pos in x if pos.startswith('N')]))


# selecting nouns and converting to a string
df["qualifications"] = df["qualifications"].apply(lambda x: ' '.join([token for token, tag in nltk.pos_tag(x) if tag.startswith('NN')]))


# initialize lemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatize_text(text):
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

# performing lemmatization for dataset
df['qualifications'] = df['qualifications'].apply(lambda x: " ".join([lemmatizer.lemmatize(word)  for word in x.split()]))


# group the DataFrame by year
grouped = df.groupby(df['created_at'].dt.year)

# create a dictionary to store the new DataFrames
year_dfs = {}

# split the groups into separate DataFrames and store them in the dictionary
for year, group in grouped:
    year_dfs[year] = group.copy()


for year in year_dfs:
    print(year_dfs[year])
    print(year)

    # defining the number of topics
    n_topics = 3

    # 1. Latent Dirichlet Allocation (LDA):
    print('\n1. Latent Dirichlet Allocation (LDA):')

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=5, stop_words='english')
    X = vectorizer.fit_transform(df['qualifications'])

    # performing topic modeling using LDA
    lda = LatentDirichletAllocation(n_components=n_topics,  max_iter=10, learning_method='batch', random_state=0)
    lda.fit(X)

    # output of topics and words for LDA
    n_top_words = 10
    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print("Topic ", topic_idx, ":")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))



#################################TEST############################################
n_topics = 3


# 2. Latent Semantic Analysis (LSA):
print('\n2. Latent Semantic Analysis (LSA):')
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

# Create a Tf-idf vectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer on the text data
X = vectorizer.fit_transform(df['qualifications'])

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
X = vectorizer.fit_transform(df['qualifications'])

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
X = vectorizer2.fit_transform(df['qualifications'])

# Berechnen der Token-Häufigkeiten
token_counts = X.sum(axis=0).A1

# Die 10 häufigsten Token ausgeben
most_common_tokens = [vectorizer2.get_feature_names_out()[i] for i in token_counts.argsort()[-50:]]
print(most_common_tokens)
