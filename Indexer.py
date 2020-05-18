

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

# def anchorwords(json_file):
# 
#     with open(json_file) as jsonfile:
#         url = json.load(jsonfile)['url']
# 
#         bits = urllib.parse.urlparse(url) #this is a 6-tuple
# 
#         anchors = re.finditer("\w*", bits[2])
# 
#         anchors_for_url = {}
# 
#         for word in anchors:
#             if len(word.group().lower()) > 0:
#                 anchors_for_url[word.group().lower()] = 1
# 
#         for word in anchors:
#             if word.group().lower() in anchors_for_url:
#                 anchors_for_url[word.group().lower()] += 1
# 
#     return anchors_for_url

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
        if (n % 100) == 0:
            print(n)
            
        if count > 5000:
            write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
            num += 1
            count= 0
            indexer= dict()
            print("Saving File", num)
            
        #if n > 29:
        #    break
        count+= 1
    write_indexer_file(indexer, ids, f"output_indexer{num}.txt")
    write_ids_file(ids)
    print("Writing document frequencies now...")
    write_docfreq_file(indexer)
   


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
                            priority[word] += 5
                        else:
                            priority[word]= 5
        
        if headers is not None:
            for header in headers:
                sentence = header.get_text()
                for word in sentence.split(" "):
                    if word is not None:
                        if word in priority:
                            priority[word] += 5
                        else:
                            priority[word] = 5
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
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)*(\.(?:com|edu|gov|org|net|mil|int|\w{2,3}))(\\w+)?)')
    if email_pat.match(lower_token) != None:
        return lower_token
    elif ip_pat.match(lower_token) != None:
        return lower_token
    elif url_pat.match(lower_token) != None:
        return lower_token
    
    
    stemmer = PorterStemmer()
    lemmatizer =  WordNetLemmatizer()
    
    stemmed_token = stemmer.stem(lower_token)
    lem_token = lemmatizer.lemmatize(lower_token) 
    if lem_token.endswith('e'):
        itemized_token = re.split('\W', lem_token.rstrip()) 
    else:
        itemized_token = re.split('\W', stemmed_token.rstrip())
    #https://stackoverflow.com/questions/24517722/how-to-stop-nltk-stemmer-from-removing-the-trailing-e
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
            f.write(f'{k}    {v.length()} \n')
    
def load_docfreq_file(filename: str) -> {str:int}:
    freq_doc = open(filename, 'r',encoding = 'utf8')
    freq_dict = dict()
    for line in freq_doc:
        itemized_line = line.split()
        token = str(itemized_line[0])
        docfreq = itemized_line[1]
        freq_dict[token] = docfreq
    print(f"Token 1: {freq_dict['0']}")
    print("Returning document frequencies...")
    return freq_dict
        
        

def sort_indexer() -> None:
    """Deal with file managment"""
    with open("output_indexer0.txt", "r", encoding = 'utf8') as f0, \
         open("output_indexer1.txt", "r", encoding = 'utf8') as f1, \
         open("output_indexer2.txt", "r", encoding = 'utf8') as f2, \
         open("0-9_output_indexer.txt", "w", encoding = 'utf8') as w0, \
         open("A-F_output_indexer.txt", "w", encoding = 'utf8') as w1, \
         open("G-M_output_indexer.txt", "w", encoding = 'utf8') as w2, \
         open("N-S_output_indexer.txt", "w", encoding = 'utf8') as w3, \
         open("T-Z_output_indexer.txt", "w", encoding = 'utf8') as w4:
        files= [f0, f1, f2]
        write_files= [w0, w1, w2, w3, w4]
        generator_files= [parse_line(f) for f in files]
        alphabetical_indexer(generator_files, write_files)
        load_docfreq_file("doc_frequencies.txt")
        



def parse_line(open_file: 'file_object') -> ['token', 'Postings']:
    """A generator for file_objects. It makes sure to iterate through the back
    so that it adds to the beginning of the LL."""
    for line in open_file:
        line= line.split("\t")
        post= add_posting(line)
        """
        line[2]= [i.strip() for i in line[2].split("->") if len(i) > 1]
        last= eval(line[2][-1])
        post= Postings(last[0], last[1], last[2])
        if len(line[2]) > 1:
            for i in range(-2, -len(line[2]) - 1, -1):
                p= eval(line[2][i])
                post.add(p[0], p[1], p[2])
        """
        yield line[0].lower(), post
    yield None


def add_posting(line:[str]) -> "Postings":
    line[2]= [i.strip() for i in line[2].split("->") if len(i) > 1]
    last= eval(line[2][-1])
    post= Postings(last[0], last[1], last[2])
    if len(line[2]) > 1:
        for i in range(-2, -len(line[2]) - 1, -1):
            p= eval(line[2][i])
            post.add(p[0], p[1], p[2])
    return post


def starting_lines(files:['generator']) -> ['postings']:
    tokens= []
    postings= []
    for line in files:
        line= next(line)
        tokens.append(line[0])
        postings.append(line[1])
    return tokens, postings


def alphabetical_indexer(r_files:['generator'], w_files:['file_object']) -> None:
    """It iterates through previous indexes so it can create a couple of new
    indexes in alphabetical order. This way all the "a" indexes are in the
    same file"""
    tokens, postings= starting_lines(r_files)    
    letters= ["0-9", "a-f", "g-m", "n-s", "t-z"]    
    while len(r_files) > 0:
        word, similar_index= same_word(tokens)
        if len(similar_index) == 1:
            post_line= update_single(similar_index[0], r_files, tokens, postings)
        else:
            post_line= update_multiple(similar_index, r_files, tokens, postings)

        if word[0] > letters[0][-1]:
            w_files.pop(0)
            letters.pop(0)
        write_single_posting(word, post_line, w_files[0])
            

def same_word(tokens:['str']) -> str and [int]:
    """It sees what word appears first. If multiple files share
    the same first word, then return a list of their indexes"""
    first = "{"
    similar_index = []
    for n, token in enumerate(tokens):
        if token == first:
            similar_index.append(n)
        elif token < first:
            first= token
            similar_index = [n]
    return first, similar_index


def update_single(n:int, r_files:['file_objects'], tokens:['str'],
                  postings:['Posting']) -> 'Posting':
    """It will return the posting. If the next line in the file is empty,
    remove that index from the list of files, tokens, and postings"""
    post_line= postings[n]
    next_line= next(r_files[n] )
    if next_line == None:
        del r_files[n]
        del tokens[n]
        del postings[n]
    else:
        tokens[n] = next_line[0]
        postings[n]= next_line[1]
    return post_line

    
def update_multiple(indexes:[int], r_files:['file_objects'], tokens:['str'],
                    postings:['Posting']) -> 'Posting':
    """It will return the posting. If the next line in the file is empty,
    remove that index from the list of files, tokens, and postings. It does
    this if multiple files share the same next word"""
    n= indexes[0]
    post_line= postings[n]

    for i in range(1, len(indexes)):
        n= indexes[i]
        post_line.combine(postings[n])

    for i in range(len(indexes) - 1, -1, -1):
        n= indexes[i]
        next_line= next(r_files[n])
        if next_line == None:
            del r_files[n]
            del tokens[n]
            del postings[n]
        else:
            tokens[n] = next_line[0]
            postings[n]= next_line[1]
    return post_line


def write_single_posting(word:str, post_line:'Posting', f: ['file_object']) -> None:
    post_line.reset()
    f.write(word.strip() + "\t" + str(post_line.counter()).strip() + "\t")
    while post_line.finish_iterating() == False:
        f.write(" -> " + str(post_line.get_node()).strip() )
        post_line.next()
    f.write("\n")



def seek() -> None:
    """It tries to find where each letter starts in each file. Like at what position
    is the letter 'g', so it doesn't have to iterate a-f to find g"""
    with open("0-9_output_indexer.txt", "r", encoding = 'utf8') as f0, \
         open("A-F_output_indexer.txt", "r", encoding = 'utf8') as f1, \
         open("G-M_output_indexer.txt", "r", encoding = 'utf8') as f2, \
         open("N-S_output_indexer.txt", "r", encoding = 'utf8') as f3, \
         open("T-Z_output_indexer.txt", "r", encoding = 'utf8') as f4, \
         open("find_letter.txt", "w", encoding = 'utf8') as w:
        lst= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z', '{']
        files= [f0, f1, f2, f3, f4]
        t= []

        for f in files:
            t0= []
            char_number= 0
            for line in f:
                letter= line[0]
                if letter == lst[0]:
                    if letter == 'c':
                        char_number+= 1
                    t0.append(char_number)
                    w.write(letter + "\t" + str(char_number) + "\n")
                    lst.pop(0)

                char_number += len(line) + 1
            t.append(t0)
        """
        print(t)
        for f, tt in zip(files, t):
            for num in tt:
                f.seek(num)
                line= f.readline()
                print(line[:40])
            print()
        """








if __name__ == '__main__':
    start= time.time()
    json_files, names = file_paths()
    index_files(json_files, names)
    sort_indexer()
    seek()
    end= time.time()
    print(end - start)
    pass



    
