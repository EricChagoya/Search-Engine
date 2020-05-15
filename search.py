# What do we do if the user searches only for special characters or empty spaces
# Do we show them nothing or keep asking them until they ask for a valid response?

import time
from LL import Postings
import Indexer
from math import log10


def searching(t:['tinker_objects???']) -> None:
    """Gets user input and displays the top n websites"""
    partial_index= dict()
    ids= get_ids()
    seeker= seek_dict()
    num_display= 5
    while True:
        #query_terms= ["a", "b", "d"]
        query_terms= "zybook computer 4th apple n horse michael machine noctural zebra".split()
        #query_terms= "4th apple horse michael machine".split() # valid_query() #Ask user until valid 
        # Need to apply the same tokenizer rules to the query terms
        start= time.time()
#         print("ids: ", ids)
#         print()
        ranked, partial_index= search(query_terms, partial_index,
                                      seeker, num_display)
        ranked_order= decode_ids(ranked, ids, num_display)

        # Display ranked_order
        end= time.time()
        total_time= end - start
        print(total_time, "seconds")
        # Display total_time

        if len(partial_index) > 500:
            partial_index= dict()
        break



def search(query_terms:[str], partial_index:{'token':'Posting'}, seeker: {str:int},
           num_display:int) -> {'id':'score'} and {'token':'Posting'}:
    """It finds a large number of relevant websites and scores them"""
    max_look= len(query_terms) * num_display * 4
    update_partial_index(query_terms, partial_index, seeker)
    for k, v in partial_index.items():
        print('Term:', k)
        v.print_nodes()
        print()
    
    temp_ranked= dict() # Do rankings here
    # Don't change partial index
    # ranked= {id of the website:score}
    
    for k, v in partial_index.items():
#         if  v.length() <= 1000:
#             print("ID: ",v.get_id())
        count = 0
        while v.get_node() != None:
            if count < 1000:
#                 print("ID: ",v.get_id())
#                 if ranked[v.get_id()] not in ranked.keys():
                tfidf = tf_idf(partial_index, k)
#                 print("tfidf:",tfidf)
                temp_ranked[v.get_id()] = tfidf
                ++count
                v.next()
            else:
                break
#         else:
#             count = 0
#             while count < 1000:
#                 temp_ranked[v.get_id()] = v.get_score()
#                 ++count
#                 v.next()    
    
#     print("Ranked dict:",sorted(ranked.items()))
    
    sorted_ranked = sorted(temp_ranked.items(), key= lambda x:x[1], reverse=True)
    
    ranked = dict()
    for item in sorted_ranked:
        ranked[item[0]] = item[1]
    print("Ranked: ", ranked)

    for ids in ranked.keys():
        position_score= 1 # ranker.query_match(partial_index, query_terms, id, max_look)
        ranked[ids] += position_score
    
    return ranked, partial_index

def tf_idf (index_file: dict, word: str) -> float:
    '''gives term freq weighting * inverse doc freq weighting, 
    should only work for queries 2-terms and longer'''
    doc_freq = 0
#     print("index_file keys: ", index_file.keys())
     
    if word in index_file:
        doc_freq = index_file[word].length()
#         print("doc_freq: ", doc_freq)
#     print("index_file[word] score: ", index_file[word].get_score())
    tf = index_file[word].get_score() 
#     print("tf: ", tf)
    idf = 55392/doc_freq
#     print("idf: ", idf)
    new_score = 1+ log10(tf) * log10(idf)
    return new_score



def update_partial_index(query_terms:[str], partial_index:{"token":"Posting"},
                         seeker:{str:int}) -> None:
    """If query terms are in the bigger index, put them in the partial index.
    If not, don't do anything"""
    sorted_terms= [t for t in sorted(query_terms) if t not in partial_index]
    files= sorted_lookup(sorted_terms)
    count= 0
        
    for group, n in enumerate(files):
        if n > 0:
            if group == 0:
                with open("0-9_output_indexer.txt", "r", encoding = 'utf8') as f0:
                    count= find_term(f0, sorted_terms, partial_index, seeker, count, n)
            elif group == 1:
                with open("A-F_output_indexer.txt", "r", encoding = 'utf8') as f1:
                    count= find_term(f1, sorted_terms, partial_index, seeker, count, n)
            elif group == 2:
                with open("G-M_output_indexer.txt", "r", encoding = 'utf8') as f2:
                    count= find_term(f2, sorted_terms, partial_index, seeker, count, n)
            elif group == 3:
                with open("N-S_output_indexer.txt", "r", encoding = 'utf8') as f3:
                    count= find_term(f3, sorted_terms, partial_index, seeker, count, n)
            else:
                with open("T-Z_output_indexer.txt", "r", encoding = 'utf8') as f4:
                    count= find_term(f4, sorted_terms, partial_index, seeker, count, n)


def find_term(f:['file_object'], sorted_terms: [str], partial_index:{'token':'Postings'},
              seeker:{int, int}, count: int, n: int) -> int:
    """Find the term in the index for those range of letters. Add it to the partial index
    if found. If not, go to the next term"""
    f.seek(int(seeker[sorted_terms[count][0]])) #Get position of the letter
    
    while n > 0:
        line= f.readline().split("\t")
        if line[0] == sorted_terms[count]:
            partial_index[line[0]]= Indexer.add_posting(line)
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
    for k, v in sorted(ranked.items(), key= (lambda x:x[1]) ):
#         print(k,v)
        ranked_order.append(ids[str(k)])
        count+= 1
        if count >= max_urls:
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
        
    





searching('t')



