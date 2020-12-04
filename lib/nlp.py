"""
@Andrew

Holds NLP Pipe class
Run this to train the pipelines

# To Do: 
* Make the fit function - clean the data, fit the vectorizer, and then fit the model.  
"""
import pickle
import pandas as pd
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

class NLPPipe:
   
    def __init__(self, vectorizer=CountVectorizer(), tokenizer=None, cleaning_function=None, 
                 stemmer=None, model=None):
        """
        A class for pipelining our data in NLP problems. The user provides a series of 
        tools, and this class manages all of the training, transforming, and modification
        of the text data.
        ---
        Inputs:
        vectorizer: the model to use for vectorization of text data
        tokenizer: The tokenizer to use, if none defaults to split on spaces
        cleaning_function: how to clean the data, if None, defaults to the in built class
        """
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
            self.naive_clean = True
        else: 
            self.naive_clean = False
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False
        
    def splitter(self, text):
        """
        Default tokenizer that splits on spaces naively
        """
        return text.split(' ')
        
    def clean_text(self, text, tokenizer, stemmer):
        """
        A naive function to lowercase all works can clean them quickly.
        This is the default behavior if no other cleaning function is specified
        """
        cleaned_text = []
        for post in text:
            cleaned_words = []
            for word in tokenizer(post):
                low_word = word.lower()
                if stemmer:
                    low_word = stemmer.stem(low_word)
                cleaned_words.append(low_word)
            cleaned_text.append(' '.join(cleaned_words))
        return cleaned_text
    
    def fit(self, text, dirty=False):
        """
        Cleans the data and then fits the vectorizer with
        the user provided text
        """
        if dirty and self.naive_clean:
            clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        elif dirty:
            clean_text = self.cleaning_function(text)
        else:
            clean_text = text
        self.vectorizer.fit(clean_text)
        self._is_fit = True
        
    def transform(self, text, dirty=False):
        """
        Cleans any provided data and then transforms the data into
        a vectorized format based on the fit function. Returns the
        vectorized form of the data.
        """
        if not self._is_fit:
            raise ValueError("Must fit the models before transforming!")
        if dirty:
            clean_text = self.cleaning_function(text, self.tokenizer, self.stemmer)
        else:
            clean_text = text
        return self.vectorizer.transform(clean_text)
    
    def save_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        pickle.dump(self.__dict__, open(filename+".mdl", 'wb'))
        
    def load_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        if filename[-4:] != '.mdl':
            filename += '.mdl'
        self.__dict__ = pickle.load(open(filename, 'rb'))
    
    def topic_transform_df(self, raw_df, dtm, append_max=True, topic_names=None):
        """
        Appends Topics from the model to the original dataframe
        Naively returns the topic the document is most likely associated with. 
        """
        # Transforms data to get model results
        topic_results = self.model.transform(dtm)
        # Assigns Column names if passed in.  
        if topic_names:
            if len(topic_names) != topic_results.shape[1]:
                raise ValueError("Number of topic names should match number of topics!")
            else:
                columns = topic_names
        else:
            columns = ['Topic_'+str(x) for x in range(topic_results.shape[1])]

        if append_max:
            raw_df['Topic'] = topic_results.argmax(axis=1)
        else:
            topic_df = pd.DataFrame(topic_results, columns=columns, index=raw_df.index)
            raw_df = raw_df.merge(topic_df, left_index=True, right_index=True)
        return raw_df, columns
    
if __name__ == "__main__":
    pass