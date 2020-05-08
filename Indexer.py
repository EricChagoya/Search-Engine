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
            if ("ANALYST" in folders):
            #if ("DEV" in folders): #or ("ANALYST" in folders)
                directories.append(os.path.join(folders, jsons))
                names.append(str(jsons))
    return directories, names



def index_files(files:[str], names:['file']) -> None:
    """It indexes after a certain number of websites iterated and then
    dumps that information into a textfile"""
    indexer= dict()
    ids= dict()
    count= 0
    num= 0
    for n, file in enumerate(files):
        tokens, url= reader(files[n])
        ids[n]= url
        priority= priority_terms(files[n])
        for k, v in tokens.items():
            score= v[0]     # Right now score will be frequency
            if k in priority:
                score += priority[k]
                
            if k in indexer:
                indexer[k].add(score, n, v[1])
            else:
                indexer[k]= Postings(score, n, v[1])
        #if (n % 1000) == 0:
        #    print(n)
            
        if count > 700:
            write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
            num += 1
            count= 0
            indexer= dict()
            print(num)
            
        #if n > 290:
        #    break
        count+= 1
    write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
    write_ids_file(ids)


def reader(file:str) -> {'token':['count', ['position'] ] } and 'url':
    """Get the tokens from a file and count how often they appear and positions"""
    tokens= dict()
    with open(file) as jsonfile:
        file= json.load(jsonfile)
        url= file['url']
        soup= BeautifulSoup(file['content'], 'html.parser')
        count= 0
        for word in soup.get_text().split():
            token= tokenizer(word)
            if token != None:
                if token not in tokens:
                    tokens[token]= [1, [count] ]
                else:
                    tokens[token][0] += 1
                    tokens[token][1].append(count)
                count += 1
    return tokens, url


def priority_terms(file:str) -> {str:int}:
    """It sees what words are in the header/bolded to increase the score"""
    with open(file) as jsonfile:
        content = json.load(jsonfile)['content']
        headers = re.finditer("(<[Hh][123].*<\/[Hh][123]>)|(<[Hh][^tml](ead)?.*?>)", content)
        bolded = re.finditer("<.?[Bb].*<(((br \/)|(\/p)|)>)", content)
        priority= dict()
        for boldedterm in bolded:
            if boldedterm in priority:
                priority[boldedterm] += 5
            else:
                priority[boldedterm]= 5
            print(boldedterm.group())
        
        for header in headers:
            if header in priority:
                priority[header] += 5
            else:
                priority[header] = 5
            print(header.group())
            
        #if len(priority) > 1:
        #    print(priority)
    return priority


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
    mod_token = ''
    for i in itemized_token:
        mod_token += i

    if len(mod_token) >= 1:
        return mod_token.lower()


def write_indexer_file(index: {'token':'Postings'}, ids: {'str'}, filename:str) -> None:
    with open(filename, "w", encoding = 'utf8') as f:
        for k, v in sorted(index.items()):
            v.reset()
            f.write(k + "\t" + str(v.counter()) + "\t")
            while v.finish_iterating() == False:
                f.write(" -> " + str(v.get_node()))
                v.next()
            f.write("\n")


def write_ids_file(ids:{int: str}) -> None:
    filename= "ids_identifier.txt"
    with open(filename, 'w', encoding = 'utf8') as f:
        for k, v in sorted(ids.items()):
            f.write(str(k) + "\t" + v + "\n")
    





if __name__ == '__main__':
    json_files, names = file_paths()
    index_files(json_files, names)










