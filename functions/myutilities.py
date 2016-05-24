# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 20:26:33 2016

@author: Steven
"""

import os
import pandas as pd
import re
import numpy as np

#%% Get Duplicates ##########################################################

def getDuplicates(ls):
    """ Returns a set with elements that are duplicates
    
    Args:
        ls (list): list of elements
        
    Returns:
        set: set with duplicates
    
    """
    # alternative
    # set([x for x in l if l.count(x) > 1])
    
    #alternative 1
    #seen_set = set()
    #return set(x for x in ls if x in seen_set or seen_set.add(x))
    
    #alternative 2
    #return [item for item, count in collections.Counter(ls).items() if count > 1]
    
    #alternative 2
    # vc = pd.Series(ls).value_counts()
    # vc[vc > 1].index.tolist()
    
    seen = set()
    duplicate = set()
    for element in ls:
        if element not in seen:
            seen.add(element)
        else:
            duplicate.add(element)
            
    return duplicate

#%% Renaming duplicates #####################################################

def renameDuplicates(ls, ignore = set()):
    """ Rename duplicates in list (e.g. if 3 copies of B: "B", "B_1", "B_2")
    
    Args:
        ls (list): list of strings
        ignore (set): elements to ignore (not renamed). Default empty set.
        
    Returns:
        list: list of string with renamed for duplicates        
        
    """ 
    ls2 = ls[:] 
    freq ={}
    
    for i, element in enumerate(ls):
        #freq[element] = freq.get(element, 0) + 1 
    
        if element not in ignore:
            
            if element not in freq:
                freq[element] = 1
            
            #duplicate found
            else:
                ls2[i] = str(element) + "_" + str(freq[element])
                freq[element] += 1
        
    return ls2
    
    
#%% Changing permissions ####################################################

def changeWinPermissions(path):
    """ Change permissions in Windows of folder and/or files in path
     /t Performs the operation on all specified files in the current directory and its subdirectories
     
    To check permissions: (Properties > Security > Edit > Add > Everyone)
     
    Args:
        path (str): path to folder of file
    
    Returns:
        none: changes the permisssion
     
    """
    
    os.system('icacls "{path_name}" /grant Everyone:F /t'.format(path_name = path))

#%% Combine dataframes ######################################################

def combineDF(files_list, files_dir_path, converters = {}):
    """ Concatenates excel files given list of filenames, path directory
    
    Args:
        files_list (list): list of files (e.g. ['a.xls','b.xls'])
        files_dir_path (str) : path where files located
        converters (dict): optional, key = column name, value = data type 
        
    Returns:
        pandasDataFrame
    """
    combined = pd.concat([pd.read_excel(os.path.join(files_dir_path, file_name), sheetname =0, converters = converters)
        for file_name in files_list])
    
    return combined

#%% Change column position ##################################################

def changeColumnPosition(column_names, column, newposition):
    """ Returns the column names list after changing position of column
    """
    column_names.insert(newposition, column_names.pop(column_names.index(column)))
    
    return column_names
    
def moveColumnsBeginning(column_names, columns):
    """ Move the columns to the beginning in the given order"""
    
    cols = [col for col in column_names if col not in columns]
    
    return columns + cols

#%% String formatting #######################################################

def dictPrintFormat(d, key_name = 'Key', value_name = 'Value'):
    """ Formats a dictionary to print, which returns a string with header key name and vlaue name,
    separator, and each row is a key, value pair from the dictionary. For example:
    
    Team    Win-Record
    ------------------
    Bulls   72-10
    Cavs    5-77
    
    Args:
        d (dict): dictionary to convert to string
        key_name(str): column name
        value_name(str): column name
    
    Returns:
        str
    
    """
    
    max_len_key = len(key_name)
    max_len_val = len(value_name)
    
    for k, v in d.items():
        if len(str(k)) > max_len_key:
            max_len_key = len(str(k))
        if len(str(v)) > max_len_val:
            max_len_val = len(str(v))
            
    header = "{key:<{key_size}}  {val:<{val_size}}".format(
               key = key_name,
               val = value_name,
               key_size = max_len_key,
               val_size = max_len_val)
               
    separator = "-"*(max_len_key + max_len_val + 2)        
        
    values = "\n".join(["{key:<{key_size}}  {val:<{val_size}}".format(
                       key = k,
                       val = v,
                       key_size = max_len_key,
                       val_size = max_len_val) for k, v in d.items()])
                       
    printout = "\n".join([header, separator, values])
    
    return printout

#%% String to boolean #######################################################

def str2bool(v):
  return v.lower() in ("y", "yes", "true", "t", "1")
  
  
#%% Boolean to String #######################################################

def booleanToStr(b, s = ("Ok", "Error")):
    """ Map boolean to Str
    Args:
        b (boolean): True or False
        s (tuple): first element corresponds to True, second to false (default = "Ok", "Error")
    
    Returns:
        s (str) depending on mapping True or False
    
    """
    if b:
        return s[0]
    else:
        return s[1]
        
        
#%% Check if digits #########################################################

def checkDigit(d):
    """ Check if element is digit (e.g. "2" will return True)
    Args:
        d (str or float ...): element to check
    Returns:
        boolean: True if element is a digit, else False 
    
    """
    
    try:
        return d.isdigit()
    except:
        return False
        
#%% Match Pattern
        
def matchPattern(pattern, s):
    """ Match pattern at beginning of string. If not match, None return
    
    Args:
        pattern(re.compile): compiled pattern
        s (str): 
    
    Return:
        matched string or 
    
    """
    
    try:
        return pattern.match(s).group()
    except:
        return None

#%% Lookup in dataframe

def isInLookup(df, df_lookup, subset = None):
    """ Check if row based on subset of columns exists in other dataframe
    
    Args:
        df (pd.DataFrame): dataframe to check rows
        df_lookup (pd.DataFrame): dataframe to look up the rows
        subset (list): Only consider certain columns for identifying duplicates, by default use all of the columns
    
    Returns:
        np.array: True/False if row in df is in df_lookup based on subset columns
        
    """
    
    # remove duplicates (keep only 1 copy) since otherwise when joined the original 
    # table will have more rows than the original number of rows
    if subset == None:
        df_lookup = df_lookup.drop_duplicates()
    else:
        df_lookup = df_lookup.drop_duplicates(subset)
        
    combined = df.merge(df_lookup, how = 'left', on = subset, indicator = True)
    combined.rename(columns = {'_merge' : 'match'}, inplace = True)
    combined['match'] = combined['match'].astype(str) # type is category
    combined['match'] = combined['match'].map(lambda x: True if x=="both" else False)
    
    return np.asarray(combined['match']) # array instead of series to avoid mismatch index with original data
    
      
#%% Logging #################################################################

import logging

class Logger:
    
    def __init__(self, logger_name, log_file, full_formatter = False):
        self.logger_name = logger_name
        self.full_formatter = full_formatter
        self.logger = logging.getLogger(logger_name)
        
        #logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        if self.full_formatter:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
        else: 
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            
        self.logger.setLevel(logging.DEBUG)
        
        # to log to file
        fh = logging.FileHandler(log_file, mode = 'w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        # to log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
    def getLogger(self):
        return self.logger
        
    def __str__(self):
        return "Logger <{logger_name}>".format(logger_name = self.logger_name)

        
#%% Test ####################################################################
        
if __name__ == "__main__":
    test = ['A', 'B', 'C', '1', 'B', '1', '2', 'B', "", ""]
    
    print(renameDuplicates(test, ignore = {""}))
    
    test_dic = {'fin_grade': 'Text',
                 'line_id': 'Text',
                 'month': 'Integer',
                 'plant_id': 'Text',
                 'variable_production_cost': 'Float'}
                 
    print(dictPrintFormat(test_dic, "column", "format"))
    
    test = pd.DataFrame({"A": [1,2,3,4], "B": [1,5,6,4], "C": [1,5,6,5]})
    test_lookup = pd.DataFrame({"A": [1,8,9,4], "B": [1,8,9,4], "C": [1,5,6,4]})
    
    print(isInLookup(test,test_lookup))
    print(isInLookup(test,test_lookup, subset = ['A','B']))
    