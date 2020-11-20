"""
@Andrew

This module is used for cleaning the reviews of the Yelp Dataset for Topic Modeling

"""

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re
import itertools

sp = spacy.load('en_core_web_md')
def load_n_lines(filepath, n):
    """
    Loads n lines from a json file.
    Returns DataFrame

    Used for testing cleaning function
    """
    f = open(filepath)
    data = []
    for line in itertools.islice(f, n):
        line = line.strip()
        if not line: continue
        data.append(json.loads(line))
    f.close()
    data = pd.DataFrame(data)
    return data

def remove_stopwords(text, stopwords=STOP_WORDS):
    """
    Remove stopwords from document.  Naively uses SpaCy Stop words
    """
    text = sp(text)
    text = [token.text for token in text if token not in stopwords]
    return ' '.join(text)

def remove_digits(text):
    """
    Uses Regex to replace anything that is not an alphabetic character with an empty string
    """
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text

def lemma(text, pos_to_avoid=[]):
    """
    Lemmatize Text.  Pass in a list of POS to avoid when lemmatizing
    """
    text = sp(text)
    text = [token.lemma_ for token in text if token.lemma_ not in pos_to_avoid]
    return ' '.join(text)

def clean_doc(text):
    # remove stopwords
    text = remove_stopwords(text)
    # lemmatize and remove pronouns
    text = lemma(text, ['-PRON-'])
    # remove digits and punctuation
    text = remove_digits(text)
    # change all to lowercase
    text = text.lower()
    return text

if __name__ == "__main__":
    import pyspark
    import databricks.koalas as ks
    import json

    rdf = load_n_lines('../yelp_dataset/yelp_academic_dataset_review.json', 5)
    spark = pyspark.sql.SparkSession.builder.getOrCreate()
    reviews = spark.read.json('../yelp_dataset/yelp_academic_dataset_review.json')
    business = spark.read.json('../yelp_dataset/yelp_academic_dataset_business.json')
    business.registerTempTable('business')
    query = """
    SELECT categories, city, state, 
    """