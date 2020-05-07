


import os
import json
import re
from LL import Postings
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer, PorterStemmer
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
            #if ("ANALYST" in folders):
            if ("DEV" in folders): #or ("ANALYST" in folders)
                directories.append(os.path.join(folders, jsons))
                names.append(str(jsons))
    return directories, names



def index_files(files:[str], names:['file']) -> {'tokens':'Postings'} and {'ids':'file'}:
    """Indexer {tokens:'Postings'}"""
    t= set()
    indexer= dict()
    ids= dict()
    count= 0
    for n, file in enumerate(files):
        ids[n]= names[n]
        #tokens= reader(files[16])
        tokens= reader(files[n])

        # Here we get the bolded and header words. Give it tokens as an argument
        # Check similarity here. If not similar, then calculate the score and indexer
        
        for k, v in tokens.items():
            t.add(k)
            score= 0    # Calculate score here
            # Right now score will be frequency
            if k in indexer:
                indexer[k].add(v[0], n, v[1])
            else:
                indexer[k]= Postings(v[0], n, v[1])
        if (n % 100) == 0:
            print(n)
            
        if count > 5000:
            write_indexer_file(indexer, ids, f"output_indexer{n}.txt")
            count= 0
            indexer= dict()
            print(n)
        count+= 1
    print("Number of Websites", n)
    print("Number of Unique Tokens", len(t) )
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
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)*(\.(?:com|edu|gov|org|net|mil|int|\w{2,3}))(\\w+)?)')
    if email_pat.match(token) != None:
        return token
    elif ip_pat.match(token) != None:
        return token
    elif url_pat.match(token) != None:
        return token
#     print(url_pat.match(token))
    mod_token = ''
    
    refined_token = token.encode().decode('ascii','replace').replace(u'\ufffd','-')
    
    stemmer = PorterStemmer()
    lemmatizer =  WordNetLemmatizer()
    
    stemmed_token = stemmer.stem(refined_token)
    lem_token = lemmatizer.lemmatize(refined_token) 
    if lem_token.endswith('e'):
        itemized_token = re.split('\W', lem_token.rstrip()) 
    else:
        itemized_token = re.split('\W', stemmed_token.rstrip())
    #https://stackoverflow.com/questions/24517722/how-to-stop-nltk-stemmer-from-removing-the-trailing-e
#     print(itemized_token)
    for i in itemized_token:
        mod_token += i
        
    if len(mod_token) >= 1:
        return mod_token.lower()
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


def write_indexer_file(index: {'token':'Postings'}, ids: {'str'}, filename:str) -> None:
    with open(filename, 'w', encoding = 'utf8') as f:
        for k, v in index.items():
            v.reset()
            f.write(k + '\t')
            while v.finish_iterating() == False:
                f.write(str(v.get_node()) + " -> ")
                v.next()
            f.write("None\n")
        f.write("Unique Tokens: " + str(len(index)) )
        f.write("Unique Files:" + str(len(ids)) )





if __name__ == '__main__':
    start= time.time()
    json_files, names = file_paths()
    print("Get File Paths", time.time() - start)
    index, ids= index_files(json_files, names)
    print("Index Files", time.time() - start)
    print("Unique Tokens: ",len(index))
    print("Unique Files:", len(ids))
    #print_indexer(index)
    write_indexer_file(index, ids, "output_indexer.txt")
    end= time.time()





