# What do we do if the user searches only for special characters or empty spaces
# Do we show them nothing or keep asking them until they ask for a valid response?

import time
from LL import Postings
import merge
from math import log10
from _functools import partial



def searching(partial_index: {'token': 'Postings'}, ids:{'ids':'urls'}, seeker:{str:int},
              num_display:int, query_terms:[str], files:['file_object']) -> [str]:
    """It gets a list of the best ranked websites"""
    ranked, partial_index= search(query_terms, partial_index, seeker, num_display, files)
#     print("Length of partial index", len(partial_index))
#     print("Length of ranked:", len(ranked))
    ranked_order= decode_ids(ranked, ids, num_display)

    if len(partial_index) > 500:
        partial_index= dict()

    return ranked_order

def search(query_terms:[str], partial_index:{'token':'Posting'}, seeker: {str:int},
           num_display:int, files:['file_object']) -> {'id':'score'} and {'token':'Posting'}:
    """It finds a large number of relevant websites and scores them"""
    max_look= num_display
    if 2 > len(query_terms):
        max_look *= len(query_terms) * 4
        
#     print("before:",partial_index)
    
    update_partial_index(query_terms, partial_index, seeker, files)

#     print("after:", partial_index)
    
    temp_ranked= dict() # Do rankings here
    # Don't change partial index
    # ranked= {id of the website:score}
#     print("Partial index:",partial_index)
    
    for k, v in partial_index.items():

        count = 0
        while v.get_node() != None:
            if count < 1000:
#                 print(k,":",v.get_node())
                temp_ranked[v.get_id()] = v.get_score()
#                 print("temp_ranked",temp_ranked)
                count += 1 
                v.next()
            else:
                break
    print("temp ranked:",temp_ranked)
    
    sorted_ranked = sorted(temp_ranked.items(), key= lambda x:x[1], reverse=True)
    
    ranked = dict()
    for item in sorted_ranked:
        ranked[item[0]] = item[1]
#     print("Ranked: ", ranked)

#     for ids in ranked.keys():
#         position_score= 1 # ranker.query_match(partial_index, query_terms, id, max_look)
#         ranked[ids] += position_score
    
    return ranked, partial_index


def update_partial_index(query_terms:[str], partial_index:{"token":"Posting"},
                         seeker:{str:int}, files:['file_object']) -> None:
    """If query terms are in the bigger index, put them in the partial index.
    If not, don't do anything"""
    sorted_terms= [t for t in sorted(query_terms) if t not in partial_index]
    files_query= sorted_lookup(sorted_terms)
    count= 0
        
    for group, index in enumerate(files_query):
        if index > 0:
            if group == 0:
                count= find_term(files[0], sorted_terms, partial_index, seeker, count, index)
            elif group == 1:
                count= find_term(files[1], sorted_terms, partial_index, seeker, count, index)
            elif group == 2:
                count= find_term(files[2], sorted_terms, partial_index, seeker, count, index)
            elif group == 3:
                count= find_term(files[3], sorted_terms, partial_index, seeker, count, index)
            else:
                count= find_term(files[4], sorted_terms, partial_index, seeker, count, index)


def find_term(f:['file_object'], sorted_terms: [str], partial_index:{'token':'Postings'},
              seeker:{int, int}, count: int, n: int) -> int:
    """Find the term in the index for those range of letters. Add it to the partial index
    if found. If not, go to the next term"""
    f.seek(int(seeker[sorted_terms[count][0]])) #Get position of the letter
    
    while n > 0:
        line= f.readline().split("\t")
        if line[0] == sorted_terms[count]:
            partial_index[line[0]]= merge.new_posting(line)
            count += 1
            n -= 1
            if (len(sorted_terms) != count) and (sorted_terms[1][0] != line[0]):
                f.seek(int(seeker[sorted_terms[count][0]]))
        elif line[0] > sorted_terms[count]:
            count += 1
            n -= 1
            if (len(sorted_terms) != count) and (sorted_terms[1][0] != line[0]):
                f.seek(int(seeker[sorted_terms[count][0]]))
    return count

def sorted_lookup(terms:[str]) -> ['str']:
    """It sees which file to look at for each query term. It returns
    a list of how often that word appears in the file"""
    files= [0, 0, 0, 0, 0]
    for letter in terms:
        letter= letter[0]
        if letter < 'a':
            files[0] += 1
        elif letter < 'g':
            files[1] += 1
        elif letter < 'n':
            files[2] += 1
        elif letter < 't':
            files[3] += 1
        else:
            files[4] += 1
    return files


def get_ids() -> {int:str}:
    """It gets the ids and the websites they are associated with"""
    file= "ids_identifier.txt"
    ids= dict()
    with open(file, "r", encoding = 'utf8') as f:
        for line in f:
            line= line.split()
            ids[line[0]]= line[1]
    return ids

def decode_ids(ranked:{int:int}, ids:{int:str}, max_urls:int) -> [str]:
    """Returns a list of urls sorted by the highest ranking first"""
    ranked_order= []
    count = 0    # Maybe enumerate
    for k, _ in sorted(ranked.items(), key= (lambda x:x[1]), reverse = True ):
#         print(k,v)
        ranked_order.append(ids[str(k)])
        count+= 1
        if count >= max_urls:
            return ranked_order
    return ranked_order


def seek_dict() -> {'letter':int}:
    """It read a file that says where each
    letter is positioned"""
    file= "find_letter.txt"
    seeker= dict()
    with open(file, "r", encoding= "utf8") as f:
        for line in f:
            line= line.split()
            seeker[line[0]]= line[1]
    return seeker
        
    





# searching('t')



