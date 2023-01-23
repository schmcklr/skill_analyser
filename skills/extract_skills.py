# extracting skills
from skills.create_skill_list import skills


def extract_skills(df_column):
    df_column = df_column.apply(lambda x: " ".join(x for x in x.split() if x in skills))
    return df_column
