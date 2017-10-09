import downloadscript as dl
import SplitFile as spl
import rewrite as rew



for num in range(1,3):
    number = "{:04}".format(num)
    filename = "medline" + number
    extfile = dl.dlext(num)
    splittedfilepath = './output/splitted/' + filename
    spl.splitxml(extfile,splittedfilepath)
    
