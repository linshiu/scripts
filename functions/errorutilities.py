# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import logging

#sys.path.insert(0,os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))  # two directories up for functions
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) + '/' + '..')  # one directory up for functions

# can also do this since same directory--> from myutilities import booleanToStr
from functions.myutilities import booleanToStr

# logger = logging.getLogger(__name__)
# Because you create the logger at module level, you then import the
# module before you load the logging configuration from a file.
# The logging.fileConfig and logging.dictConfig disables existing loggers by default.
# So, those setting in file will not be applied to your logger. It’s better to get the logger when you need it.
# By doing that, the loggers will be created after you load the configuration. The setting will be applied correctly
# ALTERNATIVE: disable_existing_loggers: False in config file
# http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python

class ErrorReports:
    """ Class to generate error reports based on original dataframe and error dataframe
    
    Error Dataframe: dataframe with column name = error, values = True/False if that row has error
    
    Result of generating dataframe is the original dataframe with error columns attached (convert to OK/ERROR)
    and original dataframe with error columns attached but only rows with at least one error
    
    Results can be exported to CSV or PG
    
    """
    
    def __init__(self, logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.data = {} # key: report_name, value: dictionary key: original df, and error_Df
        self.error_reports = {}
    
    def addReport(self, report_name, original_df, error_df):
        self.data[report_name] = {'original_df': original_df,
                                  'error_df': error_df}
        
    def generateReports(self):
        
        for report_name in self.data:
            
            error_df = self.data[report_name]['error_df'].applymap(lambda x: booleanToStr(x, ("Error", "Ok")))
            
            # join on index 
            self.error_reports[report_name] = self.data[report_name]['original_df'].join(error_df)
            
    def exportReportsCSV(self, folder_path):
        for report_name in self.error_reports:
            
            rows_error = self.data[report_name]['error_df'].any(axis = 1)
            
            self.error_reports[report_name].to_csv(os.path.join(folder_path, report_name + '_error.csv'),index = False)
            self.error_reports[report_name][rows_error].to_csv(os.path.join(folder_path, report_name + '_error_only.csv'),index = False)

            self.logger.info("Error report exported to CSV for: " + report_name)
    
    def exportReportPG(self, engine, schema):
        for report_name in self.error_reports:
            
            rows_error = self.data[report_name]['error_df'].any(axis = 1)
            
            self.error_reports[report_name].to_sql(report_name + '_error', engine, schema=schema, index=False, if_exists='replace')
            self.error_reports[report_name][rows_error].to_sql(report_name + '_error_only', engine, schema=schema, index=False, if_exists='replace')
            
            self.logger.info("Error report exported to Postgres for: " + report_name)
            

if __name__ == '__main__':
    
    error_reports = ErrorReports()
    
    # generate data
    test = pd.DataFrame({"col1": range(10)})
    
    # checks
    rows_greater_8 = test["col1"] > 8
    rows_not_even = ~ (test["col1"] % 2 == 0)
    
    # create rerport
    error_col_to_value = {"greater_8" : rows_greater_8,
                          "not_even" :  rows_not_even }
                          
    error_df = pd.DataFrame(error_col_to_value)
    error_reports.addReport('test_error_report', test , error_df)

    error_reports.generateReports()
    
    error_reports.exportReportsCSV(os.path.join(os.getcwd(),'outputs'))

