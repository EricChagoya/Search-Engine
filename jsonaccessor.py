#write a python program that will return the paths of the .json files
import os
import json
import re
#I can assume that this python module will be in the same path as the ANALYST and DEV
#folders

#Cycle through content in .json files.  Read the contents; get the tokens and
#call the indexer
def file_paths():
    directories = []

    root_directory = os.path.dirname(__file__)

    for folders, subfolders, files in os.walk(root_directory, topdown= False):

        for jsons in files:
            if ("ANALYST" in folders) or ("DEV" in folders):
                directories.append(os.path.join(folders, jsons))

    return directories


#first function:
#dictionary and .jsons as parameters | def function()
#read the .json files in the "content" key | open and read json files
#iterate through the content (split it at \n) | [] of lines

#iterate through the lines
#iterate through words
#no need to return

#different function
#check a second time for bolded and headers (can use regex for bolds and headers) | list
#label the string as either bolded or header
#if bold or header:
#indexer function prameters = (tokens, weight = 'bolded'/'header' (or True or False) [default = None])
#(plan: pass words and dictionary into indexer function)
#ψάξτε αυτές τις λέξεις:
#h1 
#h2
#h3
#headings (unlikely)
#header
#<b> <\b>
def priority_terms(file, dictionary):

    print(file)
    print("----------------------")
    with open(file) as jsonfile:

        content = json.load(jsonfile)['content']

        headers = re.finditer("(<[Hh][123].*<\/[Hh][123]>)|(<[Hh][^tml](ead)?.*?>)", content)
        #bolded = re.finditer("<.?[Bb]>.*((<[brBr] \/>)|(</[Bb]>))", content)
        bolded = re.finditer("<.?[Bb].*<(((br \/)|(\/p)|)>)", content)

        for boldedterm in bolded:
            print(boldedterm.group())

        for header in headers:
            print(header.group())
    return

def reader(file, dictionary):

    with open(file) as jsonfile:
        content = json.load(jsonfile)['content']

        individual_lines = content.split('\n') #create a list where every entry is a line

        for single_line in individual_lines:
            #some lines are empty and are displayed as "" in the list
            #this code will skip those empty strings
            single_line = single_line.strip()
            if len(single_line) >= 1:
                words = single_line.split(" ")

                for single_word in words:
                    if len(single_word) >= 1:
                        print("Possible argument: ", single_word)

    return


if __name__ == '__main__':
    #json_files = file_paths()

    #reader(json_files[8], {})

    #demonstrate that some files might not have headers or bolded text at all
    #priority_terms(json_files[16], {})
    
    #test unusual headers
    #priority_terms(json_files[128], {})

    #priority_terms(json_files[1742], {})