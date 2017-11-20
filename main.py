import downloadscript as dl
import SplitFile as spl
import rewrite as rew
import time
import os

counterfile = './logs/currentcounter.log'
logfile = "./logs/logfile.log"
if not os.path.exists(counterfile):
    fr = open(counterfile,"w+")
    fr.write("1")
    fr.close()

with open(counterfile,"r") as r:
    count = int(r.readline())

for num in range(count,10):
    try:
        number = "{:04}".format(num)
        foldername = "medline17n" + number
        logs = open(logfile,"a+")
        print("WTF")
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
        # fr2.close()
        
    

