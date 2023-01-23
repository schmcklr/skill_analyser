# preprocessing data
from bs4 import BeautifulSoup
from dataImport import job_data

# user info
print('Preprocessing job advertisements...')

# import of jobData from dataImport
jobDataCleaned = job_data

# specifies job keywords
jobKeywords = ["bpm", "process"]

# filter dataframe by keywords in column 'title' (ignores case)
jobDataCleaned = job_data[job_data['title'].str.contains('|'.join(jobKeywords), case=False)]

# keywords identifying expected skills of the job posting
skillKeywords = ["qualification", "qualifications", "competence", "competencies",
            "skill", "skills", "requirement", "requirements"]

# filter for job descriptions with skillKeywords
#jobDataCleaned = jobDataCleaned[jobDataCleaned['description'].str.contains('|'.join(skillKeywords), case=False)]


# function for cutting of text before a skillKeyword
def split_text(text, keywords):
    for keyword in keywords:
        if text and keyword in text:
            return text.split(keyword)[1]
    return None


# remove text before keyword
#jobDataCleaned['splitDescription'] = jobDataCleaned['description'].apply(lambda x: split_text(x, skillKeywords))


# remove HTML tags from text column and search by keyword
#jobDataCleaned['ul_elements'] = jobDataCleaned['splitDescription'].apply(lambda x: BeautifulSoup(x,'html.parser').find_all('ul') if x else None)
#jobDataCleaned['ul_elements'] = jobDataCleaned['ul_elements'].apply(lambda x: str(x[0]) if x else None)
#jobDataCleaned['qualifications2'] = jobDataCleaned["ul_elements"]
#jobDataCleaned = jobDataCleaned.dropna(subset=["qualifications2"], axis=0)


jobDataCleaned['qualifications2'] = jobDataCleaned["description"]
jobDataCleaned = jobDataCleaned.dropna(subset=["qualifications2"], axis=0)

print(jobDataCleaned['qualifications2'])

# function for removing html tags from column
jobDataCleaned['qualificationsCleaned'] = jobDataCleaned['qualifications2'].str.replace('<[^<]+?>', '', regex=True)


jobDataCleaned['qualifications'] = jobDataCleaned['qualificationsCleaned']
print(jobDataCleaned[(jobDataCleaned.qualifications != 'and')])
preprocessedJobData = jobDataCleaned

# export dataframe to excel file
#df.to_excel('example.xlsx', index=False)


