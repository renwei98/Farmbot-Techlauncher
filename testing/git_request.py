
import requests
from os import getcwd


filename = getcwd() + 'somefile.py'
#put the file under the current working directory
url = 'https://raw.githubusercontent.com/zizhenghuang/Farmbot-Techlauncher/master/Test%20Code/gitget.py'
#use the "raw" or the full github view of the file will be downloaded, not just the contents
r=requests.get(url)

with open(filename,'wb') as f:
    f.write(r.content)


