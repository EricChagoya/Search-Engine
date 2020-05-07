
import os
import json
import re
from bs4 import BeautifulSoup

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
    print("print to text file for easy access")

    with open(file) as jsonfile:

        content = json.load(jsonfile)
        

        json_text = open("textfile.txt", "w")
        json_text.write(content['url'])
        json_text.write(content['content'])
        json_text.close()

        soup = BeautifulSoup(content['content'], 'html.parser')
        
        
        headers = soup.find_all(re.compile("^[Hh][1-9]$"))
        bolded = soup.findAll("b" )

        print(headers)
        print(bolded)



        '''headers = re.finditer("(<[Hh][123].*<\/[Hh][123]>)|(<[Hh][^tml](ead)?.*?>)", content)
        #bolded = re.finditer("<.?[Bb]>.*((<[brBr] \/>)|(</[Bb]>))", content)
        bolded = re.finditer("<.?[Bb].*<(((br \/)|(\/p)|)>)", content)

        for boldedterm in bolded:
            print(boldedterm.group())

        for header in headers:
            print(header.group())'''
    return

def reader(file, dictionary):

    with open(file) as jsonfile:
        content = json.load(jsonfile)['content']
        soup= BeautifulSoup(content, 'html.parser')
        for text in soup.get_text().split():
            print(text)

    return


if __name__ == '__main__':
    json_files = file_paths()

    #reader(json_files[16], {})

    #demonstrate that some files might not have headers or bolded text at all
    #priority_terms(json_files[16], {})
    
    #test unusual headers
    #priority_terms(json_files[128], {})

    #priority_terms(json_files[1742], {})

    #Some stuff between the headers may not be useful
    #priority_terms(json_files[16830], {})

    #Bolded that might not be useful
    #priority_terms(json_files[30069], {})

    #What should I do with these headers?
    #priority_terms(json_files[4748], {})

    #small example of stuff between headers not being useful
    #priority_terms(json_files[34798], {})

    #json file that has no header nor bolded tags.
    #priority_terms(json_files[38021], {})
    #reader(json_files[38021], {})

    #Great example for bolded terms
    #priority_terms(json_files[23191], {})