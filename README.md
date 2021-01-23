# What do Data Scientists Blog about?
### Abstract
Pivoting careers may seem like a daunting task to some.  In addition to learning new things, you also need to learn the language,  how do you communicate in the community?  Can I help others who are interested in persuing data science take a peak into the profession?  To do this, I wanted to explore the articles highlighted in TowardsDataScience (TDS).  This project breaks down all 35000+ blog posts on TDS into 10 separate documents using two methods.  
1. A document-term matrix is reduced in dimensionality to 30 subtopics using Non-Negative Matrix Factorization
2. Docment Vectors are extracted and clustered based on their cosine similarity.  

### Summary
NLP Analysis on Towards Data Science Blogs.
Sometimes picking a project is difficult;
Someone should make a program that generates project ideas. 
So, I decided to give it a shot!

### Impact
For this project I will do a NLP analysis of the 35000+ articles published in the Towards Data Science publication.  The cross-section of problems to be solved and tools we can use to solve them is huge and we often look online for inspiration.  Sometimes landing onto the Medium publication.  Using those blog posts, I want to provide insight into:
* rising topics in popularity
* past topics and projects
* how are data scientists talking within the community

My goal is to organize the articles into unique clusters and to provide a commentary on the context of the publication. 

### Data
35000+ articles published on the TowardsDataScience publication prior to 11/19

### Methodology
1. Web Scrape articles into PostgreSQL
2. Clean articles with NLTK
3. Group Document Embeddings with Doc2Vec and NLTK KMeans
4. Topic Model cleaned articles with TF-IDF-NMF
5. Tableau Analysis

### Technologies
* Apache Spark
* Pyspark
* SciKitLearn
* NLTK
* Gensim
* PostgreSQL
* Tableau
### Next Steps

### Directory

```bash
Metis-Project-5  
--lib  
  |--NMF_topic_modeling.ipynb # Topic Modeling Notebook  
  |--cleaning.py # cleaning functions for preparing data  
  |--db_setup.sql # SQL Function for defining Schemas for Postgres  
  |--doc2vec_clustering.ipynb # Grouping of topic Models  
  |--nlp.py # NLP Pipeline Class  
  |--scraping.py # Scraping Towards Data Science  
  |--train_LDA.py # Training Pyspark LDA  
  |--train_doc2vec.py # Training Gensim Doc2Vec  
  |--validation.ipynb # Confirmation of Results  
  |--vis_util.py # Visual utility functions  
  |--work  
  |   |--tds_doc2vec_prototype.ipynb  
  |   |--tds_scraping_prototype.ipynb  
  |   |--tm_preparation.ipynb  
  |   |--topic_model_prototype.ipynb  
--readme.md  
--tds_topic_modeling_deck.pdf
```

*note: the models and dataframes are not uploaded to github because of their size.  If you choose to reproduce this project, you will have to create your own PostgreSQL database using the schemas outlined in db_setup.sql*
