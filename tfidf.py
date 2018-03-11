from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#filepath = xml file you want to count tfidf
#tag = xml tags you want to use as a train set, input as list
#returns the sparse matrix of the tf idf
def train_tfidf(filepath,tag):
    filepath = './src/test.xml'
    context = ET.iterparse(filepath)
    txt = [x.text for event,x in context if x.tag in tag ]

    count_vect = CountVectorizer()
    train_count = count_vect.fit_transform(txt)

    tfidf_transformer = TfidfTransformer()
    train_tfidf = tfidf_transformer.fit_transform(train_count)
    
    return train_tfidf

