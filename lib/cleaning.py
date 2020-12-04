"""
@Andrew

This module is used for cleaning the reviews of the Yelp Dataset for Topic Modeling

"""

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re
import itertools

sp = spacy.load('en_core_web_md')

def remove_stopwords(text, stopwords=STOP_WORDS):
    """
    Remove stopwords from document.  Naively uses SpaCy Stop words
    """
    text = sp(text)
    text = [token.text for token in text if token.text not in stopwords]
    return ' '.join(text)

def remove_digits(text):
    """
    Uses Regex to replace anything that is not an alphabetic character with an empty string
    """
    return re.sub(r'[^A-Za-z\s]', ' ', text)

def lemma(text, pos_to_avoid=[]):
    """
    Lemmatize Text.  Pass in a list of POS to avoid when lemmatizing
    """
    text = sp(text)
    text = [token.lemma_ for token in text if token.lemma_ not in pos_to_avoid]
    return ' '.join(text)

def remove_emojis(text):
    """
    Remove emojis from text
    """
    return re.sub(r':\w*:', '', text)
def remove_multiple_spaces(text):
    """
    Remove multiple consecutive spaces from text
    """
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def clean_doc(text):

    # remove emojis
    text = remove_emojis(text)
    # lemmatize and remove pronouns
    text = lemma(text, ['-PRON-'])
    # remove digits and punctuation
    text = remove_digits(text)
    # change all to lowercase
    text = text.lower()
    # remove stopwords
    text = remove_stopwords(text)
    # remove blank spaces
    text = remove_multiple_spaces(text)
    
    return text

def clean_subtitle(df):
    """
    Replace subtitle with None if Author's name appears in Subtitle
    Some subtitles scraped have the author's signature as well. 
    Ex: "by Jose Marcial Portilla"

    args: 
        df (DataFrame): Pandas Dataframe with the necessary columns
    returns: 
        None: Operation happens inplace.
    """
    assert "author" in df.columns, 'Be sure to include the author in the columns'
    assert "subtitle" in df.columns, 'Be sure to include the subtitle in the columns'

    ### Is there a faster way to "map" this function?
    for idx, row in df.iterrows():
        if re.search(str(row['author']), str(row['subtitle'])):
            df.iloc[idx]['subtitle'] = None

def sql_delete_duplicates(conn):
    query = """
    DELETE FROM towards_ds
    WHERE article_id NOT IN 
    (
        SELECT MAX(article_id) 
        FROM towards_ds 
        GROUP BY body
    );
    """
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(query)
    cursor.execute("commit;")
    
def sql_to_csv(filepath, conn):
    query = f"""
    COPY towards_ds 
    to {filepath}
    DELIMITER ',' CSV HEADER;
    """
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(query)
    cursor.execute("commit;")

    

if __name__ == "__main__":
    import sqlalchemy
    import psycopg2
    import pyspark
    import pandas as pd

    conn=psycopg2.connect(database='DS_Articles', user='postgres', host='127.0.0.1', port= '5432')
    query = """SELECT * FROM towards_ds;"""
    df = pd.read_sql_query(query, conn)
    df.body = df.body.apply(lambda row: " ".join(row.replace('{"', '').replace('"}', '').split('","')))
    # df.to_csv("../src/TDS_articles.csv", columns=df.columns, sep=',')
    df['clean_body'] = df.body.apply(clean_doc)
    df.to_csv("../src/TDS_articles_clean.csv", columns=df.columns, sep=',')
    # Uncomment this if you have duplicates in your raw data! 
    # sql_delete_duplicates(conn)
    
    # Uncomment this to save sql as CSV
    # Be Sure to change the filepath!
    # sql_to_csv('/Users/andrew/Metis-Project-5/src/TDS_articles.csv', conn)
    # query  = """SELECT * FROM towards_ds LIMIT 5"""
    # docs = pd.read_sql_query(query, conn)
    # conn.close()

    # Clean Subtitle
    # clean_subtitle(docs)
    # docs["cleaned_body"] = docs["body"].apply(clean_doc)

    # spark = pyspark.sql.SparkSession.builder.getOrCreate()
    # spark.getActiveSession()
    # articles = spark.read.csv("../src/TDS_articles.csv", header=True, inferSchema=True, sep=',')
