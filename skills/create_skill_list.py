from skills.get_skills_from_api import skills

# TODO: Currently only own defined skills are used because of testing purpose
skills = []

# creating own skill list
other_skills = ['python', 'c++','c','r','java','hadoop','scala','flask','pandas','spark','scikit-learn',
                'numpy','php','sql','mysql','css','mongdb','nltk','fastai', 'keras', 'pytorch','tensorflow',
                'linux','ruby','javascript','django','react','reactjs','ai','ui','tableau','crm', 'modeling',
                'bpm', 'vision', 'communication', 'analysis', 'design',
                'governance', 'police', 'simulation', 'automation']

# creating composed skills (needed for lemmatization that words considered as one word)
composite_skills = ['process modeling', 'application development', 'change techniques', 'business case']

# extending skill list fetched from API
skills.extend(other_skills)
skills.extend(composite_skills)