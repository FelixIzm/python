from os import listdir
from os.path import isfile, join
mypath="E:\\Temp\\obd\\"
onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
for ff in onlyfiles:
    print(ff)