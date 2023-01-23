# import and preprocessing of job advertisements
import nltk
import pandas as pd
from googletrans import Translator
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

# user info
from preprocessing.data_translation import translate_job_description, translated_job_ads, all_job_adds

print('Loading job advertisement data...')

# TODO: just for developing context, remove afterwards
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# fetching raw data
workbook = 'https://github.com/schmcklr/skillAnalyser/blob/main/jobData/jobAdvertisements.xlsx?raw=true'

# import of tabs
job_data = pd.read_excel(workbook, sheet_name="data")

# copying unformatted job description
job_data['rawDescription'] = job_data['description']

# convert text to lower case
job_data = job_data.apply(lambda x: x.astype(str).str.lower())

# elimination of duplicates
job_data = job_data.drop_duplicates(subset=["title"])
job_data = job_data.drop_duplicates(subset=["description"])

# covert 'created_at' to datetime
job_data['created_at'] = pd.to_datetime(job_data['created_at'])

# removing html tags
job_data['description'] = job_data['description'].apply(lambda x: BeautifulSoup(x.replace('\n', ' ').replace('\t', ' '), 'html.parser').get_text(separator=''))
job_data = job_data.dropna(subset=["description"], axis=0)

# removing punctuation
job_data['description'] = job_data['description'].str.replace('[^\w\s]', '', regex=True)
# remove punctuation
#jobDataRaw['description'] = jobDataRaw['description'].str.replace('[{}]'.format(string.punctuation), '', regex=True)

# initialization of translator
translator = Translator()

# user info
print('Translation of job advertisements...')


# translation of job description
job_data['title'] = job_data['title'].apply(lambda x: translate_job_description(x, 'y'))
job_data['description'] = job_data['description'].apply(lambda x: translate_job_description(x, 'n'))
print('Translation successful! ' + str(translated_job_ads) + '/' + str(all_job_adds) + ' job advertisements were translated')

# removing stopwords
stopwords = stopwords.words('english')
job_data['description'] = job_data['description'].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords))

# removing more stop words
other_stop_words = ['good', 'drive', 'part', 'time', 'develop', 'one', 'well', 'help', 'opportunities', 'execution', 'requirements', 'service',
                    'people', 'within', 'ability',  'projects', 'us', 'strong', 'environment', 'product', 'customer', 'project',  'company',
                    'services', 'solutions', 'knowledge', 'celonis', 'customers', 'new', 'working', 'support', 'skills', 'experience', 'work']


job_data['description'] = job_data['description'].apply(lambda x: " ".join(x for x in x.split() if x not in other_stop_words))


# tokenize
job_data["descriptionTokenized"] = job_data["description"].apply(nltk.word_tokenize)

# function for removing tokens that only contain numbers
def remove_numeric_tokens(tokens):
    return [token for token in tokens if not bool(re.match(r'^[0-9]+$', token))]


# remove tokens that only contain numbers
job_data["descriptionTokenized"] = job_data["descriptionTokenized"].apply(lambda x: remove_numeric_tokens(x))
job_data["descriptionTokenized"] = job_data["descriptionTokenized"].apply(lambda x: " ".join(x))


print(job_data)
#job_data.to_excel('jobRawData.xlsx', index=False)
