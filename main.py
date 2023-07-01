import urllib.request
from urllib.parse import urlparse
import re
import os
import m3u8
import tqdm
folder = "./cache/"
if not os.path.exists(folder):
    os.makedirs(folder)
    print("Created Cache Folder")
else:
    for f in os.listdir(folder):
        if not f.endswith(".ts") and not f.endswith(".m3u8"):
            continue
        os.remove(os.path.join(folder, f))

url = input("url: ")
Output = input("File name: ")
if ".mp4" not in Output:
    Output += ".mp4"
name = os.path.basename(urlparse(url).path)
print("Downloading: ", end='')
print(name)
urllib.request.urlretrieve(url, folder+name)
file = open(folder+name, 'r')
urls = re.findall(r'(https?://\S+)', file.read())
file.close()
name2 = os.path.basename(urlparse(urls[0]).path)
print("Downloading: "+name2)
urllib.request.urlretrieve(urls[0], folder+name2)
playlist = m3u8.load(folder+name2).files
for f, idk in zip(playlist, tqdm.tqdm(range(len(playlist)), unit="seg")):
    try:
        urllib.request.urlretrieve(urls[0].replace(name2, "")+f, folder + f)
    except Exception as e:
        print("\nAn error occurred while downloading "+f+"\n    Err: "+str(e)+"\n    Retrying...")
        continue
print("Exporting file with FFMPEG")
os.system('ffmpeg -i "'+folder+name2+'" -acodec copy -bsf:a aac_adtstoasc -vcodec copy "'+Output+'"')
