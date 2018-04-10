# import xml.etree.ElementTree as ET
# tree = ET.parse('example.xml')
# root = tree.getroot()
# Header = ["PMID","PubDate","Title","ArticleTitle",]
# parent_map = dict((c, p) for p in tree.getiterator() for c in p)

# for child in tree.getiterator():
#     #if(child.tag is not in )
#     if(child.tag not in Header):
#         print("remove")
# for r in parent_map:
#     parent_map.remove(r)

import xml.etree.ElementTree as ET
import os
#file = xml file input(.xml)
#outfolder = folder directory that you want to store the splitted file
def splitxml(file,outfolder):
    print('splitting ' + file)
    context = ET.iterparse(file, events=('end', ))
    index = 1
    for event, elem in context:
        if elem.tag == 'PubmedArticle':
            filename = format("PubmedTool"+ str(index) + ".xml")
            index += 1
            filepath = os.path.join(outfolder, filename)
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)
            with open(filepath, 'wb') as f:
                f.write(b'<?xml version=\"1.0\" encoding=\"utf-8\"?>\n')
                f.write(b"<!DOCTYPE PubmedArticleSet SYSTEM \"http://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_170101.dtd\">\n")
                #f.write("<PubmedArticle>\n")
                f.write(ET.tostring(elem))
                #f.write("</PubmedArticle>") 