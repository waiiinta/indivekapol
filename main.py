import downloadscript as dl
import SplitFile as spl
import rewrite as rew
import time
import os

logdirectory = './logs'
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
            for toolnum in range(tool_number,30001):
                try:
                    filename = "PubmedTool"+str(toolnum)+".xml"
                    fullname = os.path.join(path, filename)
                    rew.rewrite(fullname)
                except:
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

def main():
    #download_and_unzip()
    start_folder = 30
    end_folder = 30
    #splitfile(start_folder,end_folder)
    rewrite_xml(end_folder)

main()
