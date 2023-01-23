# preprocessing data
import pandas as pd

from preprocessing.extract_skill_section import extract_skill_section
from preprocessing.remove_other_stopwords import remove_stopwords, remove_entities
from skills.create_skill_list import composite_skills
from skills.extract_skills import extract_skills
from skills.replace_composite_skills import replace_strings_in_column

# TODO: just for developing context, remove before publish
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# user info
print('Loading job advertisement data...')
# user info
print('Preprocessing job advertisements...')

# fetching raw data (preprocessed data)
workbook = 'https://github.com/schmcklr/skillAnalyser/blob/main/jobData/job_data_preprocessed.xlsx?raw=true'
# import of tabs
job_data = pd.read_excel(workbook, sheet_name="Sheet1")

# specifies job keywords
jobKeywords = ["bpm", "process"]

# filter dataframe by keywords in column 'title' (ignores case)
job_data = job_data[job_data['title'].str.contains('|'.join(jobKeywords), case=False)]

# TODO: currently not in use because currently only words which a related to a skill will be extracted,
#  whole job description will be used
# job_data = extract_skill_section(job_data, "description")

# replacing composite skills, e.g. process modeling -> process-modeling
job_data = replace_strings_in_column(job_data, 'descriptionTokenized', composite_skills)

# removing stopwords from dataframe
job_data['descriptionTokenized'] = remove_stopwords(job_data['descriptionTokenized'])

# using the with create_skill_list created dictionary to extract skills from job adds
job_data['descriptionTokenized'] = extract_skills(job_data['descriptionTokenized'])

# remove entities like names, locations, organizations, gpe
for i, row in job_data.iterrows():
    text = row['descriptionTokenized']
    filtered_text = remove_entities(text)
    job_data.at[i, 'descriptionTokenized'] = filtered_text

