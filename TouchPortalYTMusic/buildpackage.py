import argparse
import os
import json
import shutil
from zipfile import ZipFile
from os.path import basename

parser = argparse.ArgumentParser()
parser.add_argument('-f',
                    dest='file',
                    help='Define integers to perform addition',
                    type=str,
                    nargs='+',
                    default="*"
                    )

parser.add_argument("-o", dest='output', help="File name after .tpp file has been created", type=str, required=False)
args = parser.parse_args()
print(args.output)

listfiles = []

if isinstance(args.file, list):
    for files in args.file:
        if files in os.listdir(os.getcwd()):
            listfiles.append(files)
else:
    for files in os.listdir(os.getcwd()):
        listfiles.append(files)

if "entry.tp" in listfiles:
    print('Everything looks good! Starting building zip')
    with open(listfiles[listfiles.index("entry.tp")], "r") as entry:
        pluginFolder = json.loads(entry.read())["plugin_start_cmd"].split("%TP_PLUGIN_FOLDER%")[1].split("\\")[0]
    
    try:
        os.mkdir(pluginFolder)
        for f in listfiles:
            shutil.copy(f, pluginFolder)
        with ZipFile(args.output+".tpp", "w") as zipObj:
            for folderName, subfolders, filenames in os.walk(pluginFolder):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, filePath)
    except FileExistsError as e:
        print(e)
    


else:
    print("Error: entry.tp file is required for Plugins")
