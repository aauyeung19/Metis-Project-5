if __name__ == "__main__":

    import pyspark

    # start SparkSession
    spark = pyspark.sql.SparkSession.builder.getOrCreate()
    spark.getActiveSession()

    articles = spark.read.csv('../src/TDS_articles.csv', inferSchema=True, header=True, sep="\t")

    # Register cleaning function as UDF 
    from cleaning import clean_doc
    from pyspark.sql.functions import udf, split, explode, col, posexplode
    from pyspark.sql.types import *


    # add the cleaning function as a UDF
    clean_udf = udf(clean_doc)

    # make a UDF to remove the bracket delimiters
    remove_brackets = udf(lambda row: row.replace('}"', '').replace('"{"', ''))

    articles_by_paragraph = (articles
    .select('*', posexplode(split(col('body'), '","')))
    .withColumnRenamed('pos', 'p_index')
    .withColumnRenamed('col', 'paragraph')
    )

    articles_by_paragraph.show()

    # import from pyspark machine learning
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import CountVectorizer, StopWordsRemover, IDF
    from pyspark.ml.clustering import LDA


    para_train = (
        articles_by_paragraph
            .select('article_id', 'p_index', 'paragraph') # select unique identifiers
            .where(col('paragraph').isNotNull()) # ignore blank paragraphs
            .withColumn('paragraph', clean_udf('paragraph')) # clean the text
            .withColumn('paragraph', split(col('paragraph'), ' ')) # split on blank space to tokenize words
            .withColumnRenamed('paragraph', 'text') # rename column to text for pipeline
        )
    para_train.show(5)

    tf = CountVectorizer(inputCol='text', outputCol='tf_result', minDF=0.05, maxDF=0.9)
    idf = IDF(inputCol=tf.getOutputCol(), outputCol='features')
    lda = LDA(k=20, maxIter=10)
    paragraph_pipe = Pipeline(stages=[tf, idf, lda])


    para_model = paragraph_pipe.fit(para_train)



    # models will not overwrite existing ones of the same name

    """import shutil, os
    if os.path.exists("../models/articles_LDA"):
        shutil.rmtree("../models/articles_LDA")"""

    para_model.save("../models/articles_LDA_")
