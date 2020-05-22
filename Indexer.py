

import subprocess, sys
from fileinput import filename
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
 
install("bs4")
import os
import json
import re
from LL import Postings
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer, PorterStemmer
import subprocess
import sys
import time
import urllib.parse
from math import log10
import duplicate
 
def anchorwords(json_file):
 
    with open(json_file) as jsonfile:
        url = json.load(jsonfile)['url']
 
        bits = urllib.parse.urlparse(url) #this is a 6-tuple
 
        anchors = re.finditer("\w*", bits[2])
 
        anchors_for_url = {}
 
        for word in anchors:
            if len(word.group().lower()) > 0:
                anchors_for_url[word.group().lower()] = 1
 
        for word in anchors:
            if word.group().lower() in anchors_for_url:
                anchors_for_url[word.group().lower()] += 1
 
    return anchors_for_url

def file_paths() -> ['dir'] and ['files']:
    """Cycle through content in .json files.  Read the contents; get the tokens
    and call the indexer"""
    directories = []
    names= []
    root_directory = os.path.dirname(__file__)
    for folders, _, files in os.walk(root_directory, topdown= False):
        for jsons in files:
            if ("ANALYST" in folders):
#             if ("DEV" in folders): #or ("ANALYST" in folders)
                directories.append(os.path.join(folders, jsons))
                names.append(str(jsons))
    return directories, names

def get_doc_freq(files:[str]) -> None:
    """It gets the document frequencies for all tokens then
    dumps that information into a textfile"""
    traveler = dict()
    t = dict()
    n = 0
    for file in files:
        tokens, url= reader(file)
        if duplicate.check_duplicates(traveler, url, tokens) == False:
            n += 1
            traveler[url] = tokens
            for k in tokens.keys():
                if k in t:
                    t[k] += 1
                else:
                    t[k] = 1
       
    print(n)
    write_docfreq_file(t)


def index_files(files:[str], names:['file']) -> None:
    """It indexes after a certain number of websites iterated and then
    dumps that information into a textfile"""
    indexer= dict()
    traveler = dict()
    ids= dict()
    count= 0
    num= 0
    get_doc_freq(files)
    doc_freq = load_docfreq_file("doc_frequencies.txt")

    for n, file in enumerate(files):
        tokens, url= reader(file)
        ids[n]= url
        
        if duplicate.check_duplicates(traveler, url, tokens) == False:
            traveler[url] = tokens
            priority= priority_terms(file)
            anchor = anchorwords(file)
            for k, v in tokens.items():
                #score= tf_idf(tokens, k)
#                 print("tokens.items():",k,v)
#                 print("doc_freq:",k,doc_freq[k])
                score= tf_idf(v[0], int(doc_freq[k]))     # score using tf.idf
#                 score = v[0]
                if k in priority:
                    score += priority[k]
                elif k in anchor:
                    score += anchor[k]
                elif k in indexer:
                    indexer[k].add(score, n, v[1])
                else:
                    indexer[k]= Postings(score, n, v[1])
        if (n % 100) == 0:
            print(n)
            
        if count > 15000:
            write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
#             write_docfreq_file(indexer)
            num += 1
            count= 0
            indexer= dict()
            print("Saving File", num)
            
        #if n > 29:
        #    break
        count+= 1
    write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
    write_ids_file(ids)
 
def tf_idf (tf: int, doc_freq: int) -> float:
    '''gives term freq weighting * inverse doc freq weighting, 
    should only work for queries 2-terms and longer'''

    idf = 55392/doc_freq
#     print("idf: ", idf)
    new_score = 1+ log10(tf) * log10(idf)
    return new_score  


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
                token= token.lower()
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
        soup = BeautifulSoup(content, 'html.parser')

        headers = soup.find_all(re.compile("(^[Hh][1-9]$)|(header)"))
        bolded = soup.findAll("b")

        priority= dict()
        if bolded is not None:
            for boldedterm in bolded:
                sentence = boldedterm.get_text()
                for word in sentence.split(" "):
                    if word is not None:
                        if word in priority:
                            priority[word] += 0.2
                        else:
                            priority[word]= 0.2
        
        if headers is not None:
            for header in headers:
                sentence = header.get_text()
                for word in sentence.split(" "):
                    if word is not None:
                        if word in priority:
                            priority[word] += 1
                        else:
                            priority[word] = 1
    return priority


def tokenizer(token:str) -> str: 
    '''takes in a token(key) from token/freq dict
        returns a modified token
        will include stemming, removing apostrophes, 
        dealing with hyphens, IP addresses, websites, emails, phrases, special characters
    '''
    refined_token = token.encode().decode('ascii','replace').replace(u'\ufffd','-')
    lower_token = refined_token.lower()
    
    email_pat = re.compile(r'^(?:(\w{0,64})(@)(\w{1,251}).(com))$')
    ip_pat = re.compile(r'^(?:(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))$')
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)*(\.(?:com|edu|gov|org|net|mil|int|[a-z]{2,3}))(\\w+)?)')
    dec_pat = re.compile(r'^([0-9]+)(\.)?([0-9]+)$')
    if email_pat.match(lower_token) != None:
        return lower_token
    elif ip_pat.match(lower_token) != None:
        return lower_token
    elif url_pat.match(lower_token) != None:
        return lower_token
    
    if ((lower_token[-1] in ")]") and (lower_token[0] not in "([")):
        lower_token = lower_token[0:-1]
    if dec_pat.match(lower_token) != None:
        return lower_token
    
    stemmer = PorterStemmer()
    lemmatizer =  WordNetLemmatizer()
    
    stemmed_token = stemmer.stem(lower_token)
    lem_token = lemmatizer.lemmatize(lower_token) 
    
    if lem_token.endswith('e'):
        itemized_token = re.split('\W', lem_token.rstrip()) 
    else:
        itemized_token = re.split('\W', stemmed_token.rstrip()) #https://stackoverflow.com/questions/24517722/how-to-stop-nltk-stemmer-from-removing-the-trailing-e
    mod_token = ''
    for i in itemized_token:
        mod_token += i

    if len(mod_token) >= 1:
        return mod_token
    

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

def write_docfreq_file(index: {'token': 'Postings'}) -> None:
    filename = 'doc_frequencies.txt'
    print('working')
    with open(filename, 'w', encoding = 'utf8') as f:
        for k,v in sorted(index.items()):
            f.write(f'{k}    {v} \n')
    
def load_docfreq_file(filename: str) -> {str:int}:
    freq_doc = open(filename, 'r',encoding = 'utf8')
    freq_dict = dict()
    for line in freq_doc:
        itemized_line = line.split()
        token = str(itemized_line[0])
        docfreq = itemized_line[1]
        freq_dict[token] = docfreq
#     print(f"Token 1: {freq_dict['0']}")
    print("Returning document frequencies...")
    return freq_dict
        
        

if __name__ == '__main__':
    start= time.time()
    json_files, names = file_paths()
    index_files(json_files, names)
    end= time.time()
    print(end - start)
    pass



    
