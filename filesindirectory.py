import os
import sys

path = sys.argv[1]
inside_path = os.listdir(path) 
files = []
for smth in inside_path:
    path_to_smth = os.path.join(path, smth)
    if os.path.isfile(path_to_smth):
        files.append((smth, path_to_smth))
        
def file_size(file):
    filename, path_to_file = file
    return [os.stat(path_to_file).st_size, filename]

for file in sorted(files, key=file_size, reverse=True):
    print(file[0], file_size(file)[0])
