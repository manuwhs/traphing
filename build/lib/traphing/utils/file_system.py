import os
import shutil

def create_folder_if_needed (folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def get_file_name(file_path):
    aux = file_path.split("/")
    return aux[-1]

def get_file_dir(file_path):
    aux = file_path.split("/")
    aux.pop(-1)
    
    return "/".join(aux)
    
def get_all_paths(rootFolder, fullpath = "yes"):
    ## This function finds all the files in a folder
    ## and its subfolders

    allPaths = []

    for dirName, subdirList, fileList in os.walk(rootFolder):  # FOR EVERY DOCUMENT
#       print "dirName"
       for fname in fileList:
            # Read the file
            path = dirName + '/' + fname;
            if (fullpath == "yes"):
                allPaths.append(os.path.abspath(path))
            else:
                allPaths.append(path)
    
    return allPaths


def filenames_comp(x1,x2):
    number1 = int(x1.split("/")[-1].split(".")[0])
    number2 = int(x2.split("/")[-1].split(".")[0])
    
    if (number1 > number2):
        return 1
    else:
        return -1

def filenames_comp_model_param(x1,x2):
    number1 = int(x1.split("/")[-1].split(".")[0].split(":")[-1])
    number2 = int(x2.split("/")[-1].split(".")[0].split(":")[-1])
    
    if (number1 > number2):
        return 1
    else:
        return -1

def copy_file(file_source, file_destination, new_name = ""):
    # Copies a file into a new destination.
    # If a name is given, it changes its name

    file_name = "" 
    file_path = ""
    
    file_name = file_source.split("/")[-1]
    file_path = file_source.split("/")[0]
    
    if (len(new_name) == 0): # No new name specified
        file_name = file_source.split("/")[-1]
    else:
        file_name = new_name
    
    create_folder_if_needed(file_destination)
    
    shutil.copy2(file_source, file_destination + "/" + file_name)

def remove_files(folder, remove_subdirectories = False):
    """
    This function removes all the files in a folder
    """
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif (remove_subdirectories):
                if os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)