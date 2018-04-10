import downloadscript as dl
import SplitFile as spl
import rewrite as rew
import time
import os

logdirectory = './logs'
counterfile = './logs/currentcounter.log'
logfile = "./logs/logfile.log"

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
            fr2.close()

def splitfile(start,end):  
    for num in range(start,end+1):
        if not os.path.exists('./src/split'):
            os.makedirs('./src/split')
        number = "{:04}".format(num)
        filename = "medline17n"+number+".xml"
        filelocation = "./src/raw/"+filename
        outfolder = "./src/split/"+"medline"+number
        spl.splitxml(filelocation,outfolder)

def main():
    splitfile(1,10)

main()
