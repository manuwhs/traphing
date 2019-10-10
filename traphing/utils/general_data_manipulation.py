import pandas as pd
import numpy as np
import datetime as dt

def to_numpy_2d(data):
    data = np.array(data)
    if(len(data.shape) == 1):
        data = np.atleast_2d(data).T
    elif(len(data.shape) > 2):
        raise Warning("shape wrong")
    return data

def is_numerical_array(value):
    to_numpy_array_types = [(),[],range(0,1), np.array(1), pd.Series([1]), pd.DataFrame()]
    data_types = [type(x) for x in to_numpy_array_types]
    if (type(value) in data_types):
        return True
    return False

def is_timestamp_object(value):
    """
    It detects any of the common types of date or datetime objects
    """
    to_numpy_array_types = [pd.datetime.now(), pd.datetime.today(), 
                            dt.date.today(), dt.datetime.now()]
    data_types = [type(x) for x in to_numpy_array_types]
    if (type(value) in data_types):
        return True
    return False

def is_timestamp_array(value):
    to_numpy_array_types = [pd.DatetimeIndex([0,1])]
    data_types = [type(x) for x in to_numpy_array_types]
    if (type(value) in data_types):
        return True
    return False

def is_categorical(value): 
    objects = ["a", np.array(["a"])[0]]
    data_types = [type(x) for x in objects]
    if (type(value) in data_types):
        return True
    return False

def fnp(ds):
    # This function takes some numpy element or list and transforms it
    # into a valid numpy array for us.
    # It works for lists arrays [1,2,3,5], lists matrix [[1,3],[2,5]]
    # Vectors will be column vectors
    # Working with lists
    
    # Convert tuple into list
    
    if (type(ds) == type(None)):
        return None
    if (type(ds).__name__ == "tuple"):
        ds2 = []
        for i in range(len(ds)):
            ds2.append(ds[i])
        ds = ds2
    # Convert range into list (Python 3)
    if (type(ds).__name__ == "range"):
        ds = list(ds)
        
    if (type(ds).__name__ == "list"):
        # If the type is a list 
        # If we are given an empty list 
        N_elements = len(ds)
        if (N_elements == 0):  # 
            ds = np.array(ds).reshape(1,0)
            return ds
            
        # We expect all the  elements to be vectors of some kind
        # and of the same length

        Size_element = np.array(ds[0]).size
        
            # If we have a number or a column vector or a row vector
        if ((Size_element == 1) or (Size_element == N_elements)):
            ds = np.array(ds)
    #            print ds.shape
            ds = ds.reshape(ds.size,1) # Return column vector
    
        # If we have an array of vectors
        elif(Size_element > 1):
            total_vector = []
    #            if (Size_element > N_elements):
                # We were given things in the from [vec1, vec2,...]
            for i in range(N_elements):
                vec = fnp(ds[i])
                total_vector.append(vec)
                
            axis = 1
            if (vec.shape[1] > 1):
                ds = np.array(ds)
                # If the vectors are matrixes 
                # We join them beautifully
            else:
                ds = np.concatenate(total_vector, axis = 1)
#                print "GETBE"
#                print total_vector[0].shape
#                if (Size_element > N_elements):
#                    ds = np.concatenate(total_vector, axis = 1)
#                else:
#                    ds = np.concatenate(total_vector, axis = 1).T
    # Working with nparrays
    elif (type(ds).__name__ == 'numpy.ndarray' or type(ds).__name__ == "ndarray"):

        if (len(ds.shape) == 1): # Not in matrix but in vector form 
            ds = ds.reshape(ds.size,1)
            
        elif(ds.shape[0] == 1):
            # If it is a row vector instead of a column vector.
            # We transforme it to a column vector
            ds = ds.reshape(ds.size,1)
            
    elif (type(ds).__name__ == 'DatetimeIndex'):
        ds = pd.to_datetime(ds)
        ds = np.array(ds).reshape(len(ds),1) 
    
    elif(type(ds).__name__ == 'Series'):
        ds = fnp(np.array(ds))
    
    elif (np.array(ds).size == 1):
        # If  we just receive a number
        ds = np.array(ds).reshape(1,1)
        
    return ds
    
def convert_to_matrix (lista, max_size = -1):
    # Converts a list of lists with different lengths into a matrix 
    # filling with -1s the empty spaces 

    Nlist = len(lista)
    
    listas_lengths = []
    
    if (max_size == -1):
        for i in range (Nlist):
            listas_lengths.append(lista[i].size)
        
        lmax = np.max(listas_lengths)
    else:
        lmax = max_size 
        
    matrix = -1 * np.ones((Nlist,lmax))
    
    for i in range (Nlist):
        if (lista[i].size > lmax):
            matrix[i,:lista[i].size] = lista[i][:lmax].flatten()
        else:
            matrix[i,:lista[i].size] = lista[i].flatten()
    
    return matrix

#########################################################
#################### General Data Structure ##########################
#########################################################

def windowSample (sequence, L):
    """ Transform a sequence of data into a Machine Learning algorithm,
    it transforms the sequence into X and Y being """
    
    sequence = np.array(sequence).flatten()
    Ns = sequence.size
    
    X = np.zeros((Ns - (L +1), L ))
    Y = np.zeros((Ns - (L +1),1) )
    for i in range (Ns - (L +1)):
        X[i,:] = sequence[i:i+L]
        Y[i] = sequence[i+L]
    # We cannot give the output of the first L - 1 sequences (incomplete input)
    return X, Y

def sort_and_get_order (x, reverse = True ):
    # Sorts x in increasing order and also returns the ordered index
    x = np.array(x).flatten()  # Just in case we are given a matrix vector.
    order = range(len(x))
    
    if (reverse == True):
        x = -x
        
    x_ordered, order = zip(*sorted(zip(x, order)))
    
    if (reverse == True):
        x_ordered = -np.array(x_ordered)
        
    return np.array(x_ordered), np.array(order)

def remove_list_indxs(lista, indx_list):
    # Removes the set of indexes from a list
    removeset = set(indx_list)
    newlist = [v for i, v in enumerate(lista) if i not in removeset]
    
    return newlist
