import downloadscript as dl
import SplitFile as spl
import rewrite as rew
import xml.etree.ElementTree as et
import time
import os
import search as sh
from shutil import copyfile

counterfile = './logs/currentcounter.log'
logfile = "./logs/logfile.log"
rewrite_counter ='./logs/rewrite.log'

#download_and_unzip function will download medline zip file from ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/ and unzip it.
#this function will download 100 file per time which the start file number is the last file that we already downloaded plus one.
def download_and_unzip():

    #Create log file to save the current stage of running
    if not os.path.exists(counterfile):
        os.makedirs('./logs')
        fr = open(counterfile,"w+")
        fr.write("1")
        fr.close()
    with open(counterfile,"r") as r:
        count = int(r.readline())

    for num in range(count,count+100): #Variable count got from currentcounter.log, We use it to check the start file that we already downloaded.
        try:
            number = "{:04}".format(num)
            foldername = "medline17n" + number
            logs = open(logfile,"a+")
            extfile = dl.dlext(num,logs)
            if extfile == 'DOWNLOAD FAILED':
                logs.write(foldername + "download failed\r\n")
                raise Exception(extfile)
            else:
                logs.write(foldername + "download completed\r\n")
                
            logs.close()
            counter=open(counterfile, "w")
            counter.write(str(num+1))
            counter.close()
        except Exception as e:
            print(e)
            error_logs = open(logfile,"a+")
            error_logs.write(str(e))
            error_logs.close()
            error_counter = open(counterfile, "w")
            error_counter.write(str(num))
            error_counter.close()
            break
        finally:
            logs.close()
            counter.close()

#splitfile function will split the raw xml file in the range of start and end input.
#start is the number of begining raw xml file that we want to split
def splitfile(start,end):

    #Loop of unzipped xml file that we want to split.  
    for num in range(start,end+1):
        if not os.path.exists('./src/split'):
            os.makedirs('./src/split')
        number = "{:04}".format(num)
        filename = "medline17n"+number+".xml" #name of unzipped xml file.
        filelocation = "./src/raw/"+filename #path of unzipped xml file.
        outfolder = "./src/split/"+"medline"+number #path of folder that we want to save the split file.
        spl.splitxml(filelocation,outfolder)

#rewrite_xml function will rewrite your splitted xml file with the range of last rewrite file number plus one
# and the end folder number input.
def rewrite_xml(endfolder_number):

    if not os.path.exists(rewrite_counter):
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        rw_counter = open(rewrite_counter,"w+")
        rw_counter.write("1 1")
        rw_counter.close()

    with open(rewrite_counter,"r") as r:
        folder_number,tool_number = [int(i) for i in  r.readline().strip().split()]

    for num in range(folder_number,endfolder_number+1):
            number = "{:04}".format(num)
            path = "./src/split/medline"+str(number)
            print("Rewrite split files of "+path)
            for toolnum in range(tool_number,30001):
                try:
                    filename = "PubmedTool"+str(toolnum)+".xml"
                    fullname = os.path.join(path, filename)
                    rew.rewrite(fullname)
                except:
                    print("Path : "+path)
                    print("File : "+filename)
                    fr = open(rewrite_counter, "w")
                    if toolnum == 30000:
                        toolnum = 0
                    fr.write(str(num)+" "+str(toolnum+1))
                    fr.close()
                    raise
            
            tool_number = 1
            fr = open(rewrite_counter, "w")
            fr.write(str(num+1)+" "+str(1))
            fr.close()

def fix_encode():
    fix_counter = './logs/fix.log'
    if not os.path.exists(fix_counter):
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        f_counter = open(fix_counter,"w+")
        f_counter.write("1 1")
        f_counter.close()

    f_log = open(fix_counter,'r')
    start_folder,start_tool = [int(i) for i in f_log.readline().strip().split()]
    f_log.close()

    for num in range(start_folder,465):
        print("Fix folder number : "+str(num))
        for tnum in range(start_tool,30001):
            try:
                path = "./src/split/medline"+"{:04}".format(num)
                filename = "PubmedTool"+str(tnum)+".xml"
                fullname = os.path.join(path, filename)
                rew.fix_encode(fullname)
        
            except:
                print("Path : "+path)
                print("File : "+filename)
                fr = open(fix_counter, "w")
                if tnum == 30000:
                    tnum = 0
                fr.write(str(num)+" "+str(tnum+1))
                fr.close()
                raise
        start_tool = 1    

#
#
def search_and_check_pmid(start):
    split_path = "./src/split"
    train_path = "./src/train"
    pmid_path = "./logs/pmid_search_list.txt"
    state_path = "./logs/pmid_search_state.txt"

    if not os.path.exists(pmid_path):
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        copyfile("./webcrawler/omictool_pmid.txt",pmid_path)
    
    if not os.path.exists(train_path):
        os.makedirs(train_path)
        if not os.path.exists(train_path+"/find_pmid_with_abstract"):
            os.makedirs(train_path+"/find_pmid_with_abstract")
        if not os.path.exists(train_path+"/find_no_with_abstract"):
            os.makedirs(train_path+"/find_pmid_no_abstract")

    p = open(pmid_path,'r')
    pmid_list = sorted([int(i) for i in  p.readlines()])
    p.close()

    state = open(state_path,'r')
    start_folder,start_tool = [int(i) for i in state.readline().strip().split()]
    pmid_remove =[]

    for num in range(start_folder,464):
        print('Search in medline number : '+str(num))
        med = "medline"+"{:04}".format(num)
        for tnum in range(start_tool,30001):
            pm = "PubmedTool"+str(tnum)+".xml"
            src_path = os.path.join(os.path.join(split_path,med),pm)
            print(src_path)
            try:
                tree = et.parse(src_path)
                root = tree.getroot()
                if sh.check_pmid(root,pmid_list):
                    print("Found Tool Number : "+ root.find('MedlineCitation').find('PMID').text)
                    pmid_remove.append(int(root.find('MedlineCitation').find('PMID').text))
                    if sh.check_abstract(root):
                        dst_name = med+"_"+pm
                        dst_path = os.path.join(os.path.join(train_path,"find_pmid_with_abstract"),dst_name)
                        copyfile(src_path,dst_path)
                    else:
                        dst_name = med+"_"+pm
                        dst_path = str(train_path+"/find_pmid_no_abstract"+"/"+dst_name)
                        copyfile(src_path,dst_path)
            except: 
                for pmid in pmid_remove:
                    pmid_list.remove(pmid)

                print(len(pmid_list))

                pmid_log = open(pmid_path,'w+')
                for pmid in pmid_list:
                    pmid_log.write(str(pmid)+'\n')

                state_log = open(state_path,'w+')
                state_log.write(str(num)+' '+str(tnum))
                raise
        start_tool = 1
            


def main():
    fix_encode()

main()
