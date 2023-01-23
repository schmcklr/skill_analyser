# TODO: currently not in use
# used to extract skills section
# keywords identifying expected skills of a job description
from bs4 import BeautifulSoup

skill_section_keywords = ["qualification", "qualifications", "competence", "competencies",
                          "skill", "skills", "requirement", "requirements"]


# function for cutting of text before a skillKeyword
def split_text(text, keywords):
    for keyword in keywords:
        if text and keyword in text:
            return text.split(keyword)[1]
    return None


def extract_skill_section(df, description):
    # filter for job descriptions with skillKeywords
    df = df[df[description].str.contains('|'.join(skill_section_keywords), case=False)]

    # remove text before keyword
    df['splitDescription'] = df[description].apply(lambda x: split_text(x, skill_section_keywords))

    # remove HTML tags from text column and search by keyword
    df['ul_elements'] = df['splitDescription'].apply(
        lambda x: BeautifulSoup(x, 'html.parser').find_all('ul') if x else None)
    df['ul_elements'] = df['ul_elements'].apply(lambda x: str(x[0]) if x else None)
    df = df.dropna(subset=["ul_elements"], axis=0)

    # function for removing html tags from column
    df['skill_section'] = df['ul_elements'].str.replace('<[^<]+?>', '', regex=True)

    return df
