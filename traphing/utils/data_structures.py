""" Library containing all the data structures

"""
import pandas as pd
from enum import Enum
import datetime as dt
import numpy as np

# Define the empty dataframe structure
keys = ['Open', 'High', 'Low', 'Close', 'Volume']

def get_empty_df():
    return pd.DataFrame(None,columns = keys )

keys_col = ['Symbol','Type','Size','TimeOpen','PriceOpen', 'Comision','CurrentPrice','Profit']
empty_coliseum = pd.DataFrame(None,columns = keys_col )


# Dictionary between period names and value
periods = [1,5,15,30,60,240,1440,10080,43200, 43200*12]
periods_names = ["M1","M5","M15","M30","H1","H4","D1","W1","W4","Y1"]


period_dic = dict(zip(periods,periods_names))
names_dic = dict(zip(periods_names, periods))


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

class Timeframes(Enum):
    M1 = 0
    M5 = 1
    M15 = 2
    M30 = 3
    H1 = 4
    H4 = 5
    D1 = 6
    W1 = 7
    W4 = 8
    Y1 = 9

def get_foldersData(source = "FxPro", rrf = "../" ):
    # Returns the folders where we can find the previously stored data,
    # new data to download and the info about the symbols we have or 
    # want to download.
#    rrf = "../" # relative_root_folder

    if (source == "Hanseatic"):
        storage_folder = rrf + "./storage/Hanseatic/"
        updates_folder = rrf +"../Hanseatic/MQL4/Files/"
            
    elif (source == "MQL5"):
        storage_folder = rrf + "./storage/MQL5/"
        updates_folder = rrf +"./MT5/MQL5/MQL5/Files/"
            
    elif (source == "Yahoo"):
        storage_folder = rrf +"./storage/Yahoo/"
        updates_folder = rrf +"internet"
        
    elif (source == "Google"):
        storage_folder = rrf +"./storage/Google/"
        updates_folder = rrf +"internet"

    else:
        print ("Not recognized")
    return storage_folder, updates_folder


def has__dict__(obj):
    return hasattr(obj, '__dict__')

def is_dict(obj):
    return type(obj) == type({})

def is_vector(obj):
    objects_list = [[],()]
    objects_types = [type(x) for x in objects_list]
    return type(obj) in objects_types

def is_basic(obj):
    objects_list = [1,1.0,"a", True, None, 
                    dt.date.today(), dt.datetime.now(),dt.timedelta(days= 1),
                    pd.to_datetime(dt.datetime.now()),
                    Timeframes.M1, 
                    np.array(1),np.array([1,2]), np.array([[1,2]]),
                    pd.DatetimeIndex([1,2])]
    
    objects_types = [type(x) for x in objects_list]
    return type(obj) in objects_types

def is_function(obj):
    return hasattr(obj, '__call__')

def is_DataFrame(obj):
    return type(obj) == type(pd.DataFrame())

class Node():
    """ Class that hold the information about a given object and its children
    """
    obj = None
    children = []
    level = -1
    father = None
    
    def __init__(self, obj, father, level, name):
        self.level = level 
        self.obj = obj
        self.father = father
        self.children = []
        self.name = str(name)
        
        self.class_name = "<"+str(self.obj.__class__.__name__)+">"
        
    def get_value(self):
        """ Value to show in the print"""
        return str(self.obj)[:40]
    
    def obj_print(self):
        text = self.level*"   " + str(self.class_name) + "\t" + self.name 
        if (is_basic(self.obj)):
            text += ":" +"\t"+ self.get_value()
        return text
    
    def get_children(self):
        children_list = []
        children_names = []
        
        try:
            if(is_basic(self.obj)):
                pass
            
            elif(is_DataFrame(self.obj)):
                children_list = [str(list(self.obj.columns)), self.obj.index]
                children_names = ["columns","index"]
                
            elif(has__dict__(self.obj)):
                children_list = [self.obj.__dict__[k] for k in self.obj.__dict__.keys()]
                children_names = [k for k in self.obj.__dict__.keys()]
                
            elif(is_dict(self.obj)):
                children_list = [self.obj[k] for k in self.obj.keys()]
                children_names = [k for k in self.obj.keys()]
                
            elif(is_vector(self.obj)):
                children_list = self.obj
                children_names = [self.name + "[%i]"%(i) for i in range(len(self.obj))]
                
            else:
                pass
            
            for i in range(len(children_list)):
                child = children_list[i]
                name = children_names[i]
                
                if (is_function(child) == False):
                    children_node = Node(child, self, self.level +1, name)
                    
                self.children.append(children_node)
                
        except RuntimeError:
            pass
        
        return self.children
    
        
    def print_obj_string(self):
        text = self.obj_print() + " has children:" + "\n"
        for child in self.children:
            text += child.obj_print() + "\n"
        
#        print (text)
        return text
             
def unwrap(obj, name = "object"):
    text = ""
    stack = []
    
    stack.append(Node(obj,None,0, name))
    
    while(len(stack) > 0):
        node = stack.pop(-1)
#        print("--------------------------")
#        print (node.obj)
        stack.extend(node.get_children())
        
        if (is_basic(node.obj) == False):
            text += node.print_obj_string() + "\n"
#            print ( node.print_obj_string() + "\n")
    
    print (text)
    
    



        