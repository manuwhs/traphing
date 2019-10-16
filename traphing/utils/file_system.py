import os
import shutil
from os import listdir
from os.path import isfile, join
from distutils.dir_util import copy_tree
import sys

def add_system_path(path, position = 0):
    sys.path.insert(position, path) # Adds higher directory to python modules path.
    
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
            

def export_MQL5_files(MT5_folder):
    """
    Exports the MQL5 file codes into the corresponding MLQ5 folder so that MT5 can execute them.
    """
    src_files_folder = "../traphing/MQL5/"
    MT5_folder = MT5_folder + "MQL5/"
    create_folder_if_needed(MT5_folder+"Include/traphing/")
    create_folder_if_needed(MT5_folder+"Scripts/traphing/")
    
    copied_files = copy_tree(src_files_folder, MT5_folder, update = False)
    print("Copied files from " + src_files_folder + " to " + MT5_folder)
    print("  "+ "\n  ".join(copied_files) )

def import_MQL5_files_for_library_update(MT5_folder):
    """
    Imports the modified files in the MT5 folder into the library codes for commiting changes.
    This is necessary because the MQL5 code files should be modified in the MT5 folder.
    """
    des_files_folder_include = "../traphing/MQL5/Include/traphing/"
    des_files_folder_scripts = "../traphing/MQL5/Scripts/traphing/"
    create_folder_if_needed(des_files_folder_include)
    create_folder_if_needed(des_files_folder_scripts)
    
    MT5_folder +=  "MQL5/"
    include_folder = MT5_folder + "Include/traphing/"
    scripts_folder = MT5_folder + "Scripts/traphing/"
    
    MT5_Include_files = [f for f in listdir(include_folder) if isfile(join(include_folder, f))]
    for filename in MT5_Include_files:
        if filename[-3:] == "mqh":
            shutil.copy(include_folder + filename, des_files_folder_include + filename)
            print(des_files_folder_include + filename)

    MT5_Script_files = [f for f in listdir(scripts_folder) if isfile(join(scripts_folder, f))]
    for filename in MT5_Script_files:
        if filename[-3:] == "mq5":
            shutil.copy(scripts_folder + filename, des_files_folder_scripts + filename)
            print(des_files_folder_scripts + filename)