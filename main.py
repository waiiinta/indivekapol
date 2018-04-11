import downloadscript as dl
import SplitFile as spl
import rewrite as rew
import time
import os

logdirectory = './logs'
counterfile = './logs/currentcounter.log'
logfile = "./logs/logfile.log"
rewrite_counter ='./logs/rewrite.log'

def download_and_unzip():

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
            fr=open(counterfile, "w")
            fr.write(str(num+1))
            fr.close()
        except Exception as e:
            print(e)
            fr2 = open(logfile,"a+")
            fr2.write(str(e))
            fr2.close()
            fr = open(counterfile, "w")
            fr.write(str(num))
            fr.close()
            break
        finally:
            logs.close()
            fr.close()

def splitfile(start,end):  
    for num in range(start,end+1):
        if not os.path.exists('./src/split'):
            os.makedirs('./src/split')
        number = "{:04}".format(num)
        filename = "medline17n"+number+".xml"
        filelocation = "./src/raw/"+filename
        outfolder = "./src/split/"+"medline"+number
        spl.splitxml(filelocation,outfolder)

def rewrite_xml(endfolder_number):

    if not os.path.exists(rewrite_counter):
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        fr = open(rewrite_counter,"w+")
        fr.write("1 1")
        fr.close()

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
