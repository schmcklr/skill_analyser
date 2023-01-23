from nltk import word_tokenize, pos_tag, ne_chunk

# defining other stop words
other_stop_words = ['good', 'drive', 'part', 'time', 'develop', 'one', 'well', 'help', 'opportunities', 'execution',
                    'requirements', 'service',
                    'people', 'within', 'ability', 'projects', 'us', 'strong', 'environment', 'product', 'customer',
                    'project', 'company',
                    'services', 'solutions', 'knowledge', 'celonis', 'customers', 'new', 'working', 'support', 'skills',
                    'experience', 'work',
                    'operation', 'internship', 'partner', 'value', 'client', 'company', 'online', 'market', 'field',
                    'year', 'manager', 'also',
                    'office', 'responsible', 'internal', 'looking', 'training', 'responsibility', 'quality', 'job',
                    'department', 'task', 'professional',
                    'world', 'offer', 'change', 'group', 'employee', 'implementation', 'global', 'improvement', 'area',
                    'zalando', 'fashion', 'discount',
                    'model', 'year', 'future', 'take', 'organization', 'challenge', 'expert', 'operation', 'way',
                    'information', 'use', 'relevant', 'personal',
                    'best', 'stakeholder', 'study', 'analytical', 'digital', 'performance', 'engineering',
                    'operational', 'industry',
                    'control', 'various', 'sale', 'continuous', 'need', 'across', 'career', 'improve', 'financial',
                    'role', 'standard', 'area', 'high',
                    'different', 'key', 'user', 'operation', 'level', 'make', 'diverse', 'ensure', 'company',
                    'employee', 'task',
                    'preferably', 'detail', 'overall', 'context', 'bringing', 'request', 'candidate', 'grow', 'safety',
                    'shop',
                    'unicredit', 'station' 'amazon', 'represent', 'industry', 'ag', 'merit', 'nestlé', 'advise',
                    'review', 'applicant', 'term',
                    'gain', 'description', 'everyone', 'therefore', 'shopping', 'meet', 'truck', 'portfolio', 'fruit',
                    'everyone', 'therefore', 'shopping', 'meet', 'truck', 'fruit', 'coordinate', 'may', 'derive',
                    'line', 'ready', 'owner',
                    'several', 'participate', 'step', 'transport', 'many', 'plant', 'needed', 'germany', 'largest',
                    'commercial', 'initial',
                    'capacity', 'dare', 'trainee', 'highly', 'sexual', 'without', 'operating', 'making', 'accept',
                    'asset', 'kpmg', 'origin',
                    'celebrate', 'package', 'next', 'national', 'mentoring', 'providing', 'period', 'discount',
                    'housekeeping', 'yoga',
                    'management', 'bookkeeping', 'economy', 'vocabulary', 'billing', 'operation', 'finance', 'sale']


# removing stopwords from dataframe
def remove_stopwords(df_column):
    df_column = df_column.apply(lambda x: " ".join(x for x in x.split() if x not in other_stop_words))
    return df_column


# remove names, locations, organizations, gpe
def remove_entities(text):
    ne_tree = ne_chunk(pos_tag(word_tokenize(text)))
    entities = set()
    for subtree in ne_tree.subtrees():
        if subtree.label() in ('PERSON', 'ORGANIZATION', 'GPE', 'LOCATION', 'PRODUCT'):
            entity = ""
            for leaf in subtree.leaves():
                entity = entity + leaf[0] + " "
            entities.add(entity.strip())
    for entity in entities:
        text = text.replace(entity, "")
    return text
