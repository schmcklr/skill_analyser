from googletrans import Translator
from langdetect import detect

# initialization of global variables
translated_job_ads = 0
all_job_adds = 0

# initialization of translator
translator = Translator()


# function for translation of job description
def translate_job_description(text, count):
    # global keyword to access global variables
    global all_job_adds
    if count == 'y':
        all_job_adds += 1
    if detect(text) != 'en':
        # global keyword to access global variables
        global translated_job_ads
        if count == 'y':
            translated_job_ads += 1
        translated = translator.translate(text, dest='en').text
    else:
        translated = text
    return translated
