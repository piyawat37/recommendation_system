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

def chrome_driver_path():
    directory = project_source_path() + "\\common-service\\chromedriver\\chromedriver.exe"
    return directory

def movies_image_path():
    directory = project_source_path() + "\\frontend\\src\\assets\\storage\\movies\\images\\"
    return directory