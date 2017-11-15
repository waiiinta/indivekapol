import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
def getArticle(pmid):
    src = "./src/raw/"
    for file in os.listdir(src):
        filepath = os.path.join(src,file)
        tree = ET.parse(filepath)
        root = tree.getroot()
        for pubmedArticle in root:
            medlineCitation = pubmedArticle[0]
            check = medlineCitation.find("PMID")
            if check.text == str(pmid):
                treeout = ET.ElementTree(pubmedArticle)
                treeout.write("./src/"+str(pmid)+".xml")
                return
        

getArticle(27680) 