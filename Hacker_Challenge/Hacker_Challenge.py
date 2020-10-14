#!/usr/bin/env python
# coding: utf-8

# ## Hacker Challenge 2020
# Write a 🐍 program that logs on the Hub and downloads module files.
# 
# And hopefully don't get kicked out 😅

# ## User Inputs

# In[1]:


user_username = input("Insert Username (e.g. af2230):    ")
user_password = input("Insert Password:    ")


import subprocess
import sys

def install(package):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


with open("requirements.txt") as f:
    for pk in f:
        install(pk)


# Specify the folder where you want to save the downloads
import os
download_folder_path = os.getcwd()
download_folder_path = os.path.join(download_folder_path,"Courses_Downloads") # Default

import easygui as eg

question = "What courses do you want to download?  The files will be downloaded in a folder called  'Courses_Downloads' stored in the same folder where this script is stored"
title = "Select courses"
courses = ["Math", "FDT", "DSA"]

choice = eg.multchoicebox(question , title, courses)
courses = choice

# Paths to the course File folders
paths_to_file = {"Math": "https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2Ft14inxc5bfcwaqu%2FAADiq3JtxF07oJ3ymOe94nH2a%3Fdl%3D0&iframe=false",
                 "FDT":"https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2F7w7a76i95jtl3ca%2FAADl7D_Tn6xUZ97KCdzmxl-sa%3Fdl%3D0&iframe=false",
                 "DSA":"https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2Fwji42tbpgzpfzir%2FAADnJYBolgVuVDYvJ4nI2wQla%3Fdl%3D0&iframe=false"}


# In[2]:


"""
flag_download = input("Do you want to set the folder where the files will be downloaded? (If you don't they will be downloaded in a folder called 'Downloads' located in the root of this script) - Type yes or no:  ")
while (flag_download.lower() != "yes") and (flag_download.lower() != "no"):
    flag_download = input("Type yes or no:   ")
    
from tkinter import filedialog
from tkinter import *

    
if flag_download.lower() == "yes":
    root = Tk()
    download_folder_path = filedialog.askdirectory()
    root.withdraw()
    download_folder_path = download_folder_path.split("/")
    download_folder_path = os.path.join(*download_folder_path)
    download_folder_path = os.path.join(download_folder_path,"Courses_Downloads")
else:
    pass
"""


# ### Importing selenium:webdriver and setting the browser to chrome

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys in the keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from sys import platform
if platform == "linux" or platform == "linux2":
    pass
if platform == "darwin":
    chromedriver = os.getcwd()
    chromedriver = os.path.join(chromedriver,"chromedriver") # Mac
if platform == "win32":
    chromedriver = os.getcwd()
    chromedriver = os.path.join(chromedriver,"win_chromedriver.exe") # Windows


# os.environ["webdriver.chrome.driver"] = chromedriver
chrome_options = Options()

# Turn off chrome warning for multiple downloads
prefs = {'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory" : download_folder_path}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chromedriver,options=chrome_options)


# ### Connecting to the Hub trough the Imperial Login 

# In[5]:


driver.get('https://imperial.insendi.com/auth/saml/authenticate/imp?returnPath=/')


# ### Entering the Username

# In[6]:


elem_username = driver.find_element_by_name("j_username")
elem_username.clear()
elem_username.send_keys(user_username)


# ### Entering the password and pressing "Enter"

# In[7]:


elem_password = driver.find_element_by_name("j_password")
elem_password.clear()
elem_password.send_keys(user_password)
elem_password.send_keys(Keys.RETURN)


# ### Connecting to the Dropbox folder and downloading the files

# In[8]:


for course in courses:
    dropdox_Path = paths_to_file[course]
    driver.get(dropdox_Path)
    time.sleep(3)
    driver.find_element_by_xpath("//button[@aria-label='Download']").click()
    time.sleep(3)


# ### Wait untill the downloads are finished

# In[9]:


seconds = 0
wait = True
while wait:
    time.sleep(1)
    wait = False
    for fname in os.listdir(download_folder_path):
        if fname.endswith('.crdownload'):
            wait = True
    seconds += 1
    if seconds %5 ==0:
        print("Seconds passed since the start of the downloads ",seconds)


# ### Unzipping the downloaded folders and renaming them

# In[10]:


from zipfile import ZipFile
downloads = os.listdir(download_folder_path)
downloads_zips = [i for i in downloads if ".zip" in i and "crd" not in i]
zip_paths = [os.path.join(download_folder_path,i) for i in downloads_zips]
the_len = len(zip_paths[0])
if not all(len(l) == the_len for l in zip_paths):
    zip_paths = sorted(zip_paths)
    zip_paths = zip_paths[-1:] + zip_paths[:-1] 
else:
    zip_paths = sorted(zip_paths)
    
for i,zip_fold in enumerate(zip_paths):
    with ZipFile(zip_fold, 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall(os.path.join(download_folder_path,courses[i]))


# ### Removing the .zip files

# In[11]:


for zip_path in zip_paths:
    os.remove(zip_path)

