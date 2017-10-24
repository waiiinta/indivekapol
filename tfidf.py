from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#filepath = xml file you want to count tfidf
#savevocab = where to save the list of vocabulary
#savelog = where to save the frequency
#def tfidf(filepath,savelog):
filepath = './src/test.xml'
context = ET.iterparse(filepath)
txt = [x.text for event,x in context if x.tag == 'ArticleTitle' ]

count_vect = CountVectorizer()
train_count = count_vect.fit_transform(txt)

tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_count)
print(count_vect.vocabulary_)
print(train_tfidf)