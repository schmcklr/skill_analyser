# Preprocessing, used to clean uo the job description
import pandas as pd
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from analysis.lda import analysis_with_lda
from analysis.token_freuencies import get_token_frequencies
from preprocessing.data_preprocessing import job_data, composite_skills
from visualization.data_visualization import visualization


# TODO: remove
# display options for dataframes
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)


# Define a function to keep only nouns and remove other word groups
#df['tagged_text'] = df['qualifications'].apply(lambda x: nltk.pos_tag(nltk.word_tokenize(x)))
#df['qualifications'] = df['tagged_text'].apply(lambda x: ' '.join([word for word, pos in x if pos.startswith('N')]))


# selecting nouns and converting to a string
#job_data["qualifications"] = job_data["qualifications"].apply(lambda x: ' '.join([token for token, tag in nltk.pos_tag(x) if tag.startswith('NN')]))


# initialize lemmatizer
lemmatizer = WordNetLemmatizer()
#def lemmatize_text(text):
#    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

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

# analysis based on year
for year in year_dfs:
    # TODO: remove
    print(year)
    print(year_dfs[year])

    # defining the number of topics
    n_topics = 3

    # 1. Latent Dirichlet Allocation (LDA):
    analysis_with_lda(year_dfs, year, 'descriptionLemmatized', n_topics)

    # 2. Latent Semantic Analysis (LSA):
    analysis_with_lda(year_dfs, year, 'descriptionLemmatized', n_topics)

    # initialize CountVectorizer
    count_vectorizer = CountVectorizer()
    # convert the text data into a matrix of token frequencies
    X = count_vectorizer.fit_transform(year_dfs[year]['descriptionLemmatized'])

    # 3. Token frequencies:
    get_token_frequencies(count_vectorizer, X)

    # 4. Visualization
    visualization(count_vectorizer, X, year)


