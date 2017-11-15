import downloadscript as dl
import SplitFile as spl
import rewrite as rew




for num in range(1,3):
    number = "{:04}".format(num)
    foldername = "medline17n" + number
    logfile = open("./logs/logfile.log","w+")
    extfile = dl.dlext(num,logfile)
    if extfile == 'DOWNLOAD FAILED':
        logfile.write(foldername + "download failed\r\n")
    else:
        logfile.write(foldername + "download completed\r\n")
    logfile.close()
    

