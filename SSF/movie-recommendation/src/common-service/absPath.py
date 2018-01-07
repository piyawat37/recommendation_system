'''
Created on Jan 1, 2018

@author: Piyawat Pemwattana
'''
import os

def project_source_path():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return directory

def csv_file_path():
    directory = project_source_path() + "\\python-generated\\csv-file\\"
    return directory
