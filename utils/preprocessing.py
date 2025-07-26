import re

def clean_texts(text_series):
    return text_series.apply(lambda x: re.sub(r'\W+', ' ', str(x)).lower().strip())
