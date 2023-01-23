# imports
import spacy
from spacy.matcher import PhraseMatcher
from dataImport import job_data
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
from dataPreprocessing import preprocessedJobData

nlp = spacy.load("en_core_web_lg")
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# extract skills from job_description
job_description = """
You are a Python developer with a solid experience in web development
and can manage projects. You quickly adapt to new environments
and speak fluently English and French
"""
first_entry = preprocessedJobData.iloc[0]["description"]
#annotations = skill_extractor.annotate(first_entry["description"])
#for key in annotations['results']:
#    for item in annotations['results'][key]:
#        print(item['doc_node_value'])
#print(annotations)




def get_response(row):
    annotations = skill_extractor.annotate(row)
    print(annotations)
    print(row)
    data = []
    for key in annotations['results']:
        for item in annotations['results'][key]:
            if item['doc_node_value'] not in data:
                if item['score'] == 1:
                    data.append(item['doc_node_value'])
                    print(item['doc_node_value'])
                    print(data)
    print(data)
    return data

jobDataHead = job_data.head()
jobDataHead["skills"] = jobDataHead["description"].apply(get_response)