# What do Data Scientists Blog about?
### Abstract
Pivoting careers may seem like a daunting task to some.  In addition to learning new things, you also need to learn the language,  how do you communicate in the community?  Can I help others who are interested in persuing data science take a peak into the profession?  To do this, I wanted to explore the articles highlighted in TowardsDataScience (TDS).  This project breaks down all 35000+ blog posts on TDS into 10 separate documents using two methods.  
1. A document-term matrix is reduced in dimensionality to 30 subtopics using Non-Negative Matrix Factorization
2. Docment Vectors are extracted and clustered based on their cosine similarity.  

With these document vectors trained into a model, I was able to implement a model locally.  A user can insert a new unseen article and it will return suggested tags and similar articles from the corpus. 

### Motivation
Considering more people are blogging and adding content to the blog sphere, I could expand my topic modeling to organize new documents into their respective bins.  This method can be expanded to training a model in a different domain to classify new documents.  

### Technologies
* Apache Spark
* Pyspark
* SciKitLearn
* NLTK
* Gensim
* PostgreSQL
* Tableau
* Streamlit 

### Methodology
#### Data and Prep
Data collected was all webscraped from TDS.  The articles are each scraped and inserted into a local Postgres database using [scraping.py](https://github.com/aauyeung19/Topic-Modeling-Towards-Data-Science-NLP/blob/main/lib/scraping.py).  If the scraper encountered an error or if I needed to pause the scraper, I could cross reference the links I had already scraped as to not put too much load onto Medium.com.  
Data was cleaned using methods written in [cleaning.py](https://github.com/aauyeung19/Topic-Modeling-Towards-Data-Science-NLP/blob/main/lib/cleaning.py) Clean articles and text was necessary for topic modeling with NMF.  The steps in cleaning included:
* stopword removal
* lemmatizing
* removal of emojis and digits
* removing pronouns 

#### Topic Modeling
Topic modeling was performed using TF-IDF and NMF on the entire corpus.  A separate doc2vec model was then trained on the corpus extracting document vectors from the articles using Gensim.

#### Clustering
To organize the documents into groups based on semantic similarity, I used KMeansClusterer to group together the document vectors.  I randomly subsampled my data with a shuffle split and checked different cluster sizes.  I found that 10 clusters yielded the best silhouette score.

<p align="center">
  <img alt="Silhouette Scores" src="https://github.com/aauyeung19/Topic-Modeling-Towards-Data-Science-NLP/blob/main/vis/silhouette_training.png?raw=true">
</p>

I then looked at the topic distribution from NMF inside each of the clusters.  I was able to tag them each and visualize each document vector in 3D space a TensorBoard linked [here](http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/aauyeung19/0c6e22d35cd601fbe07fa9f97ff2221c/raw/8463ec2972f8c5e6b295d2462e96b9cbb7c9a4af/projector_config.json).  Feel free to check it out and play around with the vectors projected into three dimensions! To see the labels, click the TSNE300 Bookmark on the bottom left hand corner. 

<p align="center">
  <a href="http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/aauyeung19/0c6e22d35cd601fbe07fa9f97ff2221c/raw/8463ec2972f8c5e6b295d2462e96b9cbb7c9a4af/projector_config.json">
    <img alt="Tensorboard" src="https://github.com/aauyeung19/Topic-Modeling-Towards-Data-Science-NLP/blob/main/vis/Document%20Vectors%20Screenshot.png?raw=true">
  </a>
</p>

#### Implementation 
To allow for user interaction, I set up a streamlit implementation to let users parse unread articles.  This model and practice can be extended to other domains with different articles.  If you want to attempt to run the streamlit implementation feel free to contact me and I can send you the model as it is too large to host on github.

<p align="center">
  <img alt="Streamlit Application" src="temp">
</p>

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
--src
  |--streamlit_src.csv
--vis
  |--Document Vectors Screenshot.png
  |--silhouette_training.png
--models
  |--d2v_v5.model # Insert the model here after decompressing 
--readme.md  
--tds_topic_modeling_deck.pdf
```

*note: the models and dataframes are not uploaded to github because of their size.  If you choose to reproduce this project, you will have to create your own PostgreSQL database using the schemas outlined in db_setup.sql*
