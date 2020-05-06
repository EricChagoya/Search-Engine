
import os
import json
import re
from LL import Postings
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import subprocess
import sys

import time


def file_paths() -> ['dir'] and ['files']:
    """Cycle through content in .json files.  Read the contents; get the tokens
    and call the indexer"""
    directories = []
    names= []
    root_directory = os.path.dirname(__file__)
    for folders, _, files in os.walk(root_directory, topdown= False):
        for jsons in files:
            if ("ANALYST" in folders) or ("DEV" in folders):
                directories.append(os.path.join(folders, jsons))
                names.append(str(jsons))
    return directories, names



def index_files(files:[str], names:['file']) -> {'tokens':'Postings'} and {'ids':'file'}:
    """Indexer {tokens:'Postings'}"""
    indexer= dict()
    ids= dict()
    for n, file in enumerate(files):
        ids[n]= names[n]
        #tokens= reader(files[16])
        tokens= reader(files[n])

        # Here we get the bolded and header words. Give it tokens as an argument
        # Check similarity here. If not similar, then calculate the score and indexer
        
        for k, v in tokens.items():
            score= 0    # Calculate score here
            # Right now score will be frequency
            if k in indexer:
                indexer[k].add(v[0], n, v[1])
            else:
                indexer[k]= Postings(v[0], n, v[1])
        if n > 20:
            break
    return indexer, ids


def reader(file:str) -> {'token':['count', ['position'] ] }:
    """Get the tokens from a file and count how often they appear and positions"""
    tokens= dict()
    with open(file) as jsonfile:
        content = json.load(jsonfile)['content']
        soup= BeautifulSoup(content, 'html.parser')
        count= 0
        for word in soup.get_text().split():
            token= tokenizer(word)     #Indexer(word)
            if token != None:
                if token not in tokens:
                    tokens[token]= [1, [count] ]
                else:
                    tokens[token][0] += 1
                    tokens[token][1].append(count)
                count += 1
    return tokens
                

def tokenizer(token:str) -> str: 
    '''takes in a token(key) from token/freq dict
        returns a modified token
        will include stemming, removing apostrophes, 
        dealing with hyphens, IP addresses, websites, emails, phrases, special characters
    '''
    
    email_pat = re.compile(r'^(?:(\w{0,64})(@)(\w{1,251}).(com))$')
    ip_pat = re.compile(r'^(?:(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))$')
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)?(\.(?:com|edu|gov|org|net|mil|int|\w{2,3})))')
    if email_pat.match(token) != None:
        return token
    elif ip_pat.match(token) != None:
        return token
    elif url_pat.match(token) != None:
        return token
    #print(url_pat.match(token))
    mod_token = ''
    
    refined_token = token.encode().decode('ascii','replace').replace(u'\ufffd','-')
    stemmer = PorterStemmer()
    stemmed_token = stemmer.stem(refined_token)
    itemized_token = re.split('\W', stemmed_token.rstrip())
#     print(itemized_token)
    for i in itemized_token:
        mod_token += i
        
    if len(mod_token) >= 1:
        return mod_token
    else:
        return None


def priority_terms(file) -> None:
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


def print_indexer(index:{'token':'Postings'}):
    print("Tokens\tPostings")
    count= 0
    for k, v in index.items():
        print(k, end= "\t")
        v.print_nodes()
        count+= 1
        if count > 10:
            break


def write_indexer_file(index: {'token':'Postings'}, filename:str) -> None:
    with open(filename, 'w') as f:
        for k, v in index.items():
            v.reset()
            f.write(k + '\t')
            while v.finish_iterating() == False:
                f.write(str(v.get_node()) + " -> ")
                v.next()
            f.write("None\n")





if __name__ == '__main__':
    start= time.time()
    json_files, names = file_paths()
    print("Get File Paths", time.time() - start)
    index, ids= index_files(json_files, names)
    print("Index Files", time.time() - start)
    #print_indexer(index)
    write_indexer_file(index, "output_indexer.txt")
    end= time.time()
    #print("Finish", end - start)

    #reader(json_files[8])
    #reader(json_files[16])

    #demonstrate that some files might not have headers or bolded text at all
    #priority_terms(json_files[16])
    
    #test unusual headers
    #priority_terms(json_files[128])

    #priority_terms(json_files[1742])
