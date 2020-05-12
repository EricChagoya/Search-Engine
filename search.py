# What do we do if the user searches only for special characters or empty spaces
# Do we show them nothing or keep asking them until they ask for a valid response?

import time


def searching(t:['tinker_objects???']) -> None:
    """Gets user input and displays the top n websites"""
    partial_index= dict()
    ids= get_ids()
    seeker= seek_dict()
    num_display= 5
    while True:
        query_terms= "machine" # valid_query() #Ask user until valid 

        start= time.time()
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
    ranked= update_partial_index(query_terms, partial_index, seeker)

    for ids in ranked.keys():
        position_score= 1 # ranker.query_match(partial_index, query_terms, id, max_look)
        ranked[ids] += position_score

    return ranked, partial_index





def update_partial_index(query_terms:[str], partial_index:{"token":"Posting"},
                         seeker:{str:int}) -> {'id':'score'}:
    """Put query terms in the partial index"""
    sorted_terms= [t for t in sorted(query_terms)]
    ranked= dict()
    # File shenanigans
    for t in sorted_terms:
        if t not in partial_index:
            pass
            # Find it in the file
            # It iterate through the files using seek
    return ranked




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
    count = 0	# Maybe enumerate
    for k, v in sorted(ranked.items(), key= (lambda x:x[1]) ):
        ranked_order.append(ids[k])
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



