from LL import Postings
from builtins import str
from pydoc import doc
from _operator import index
from cmath import log
from math import log10

#•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

def store_positions(index_file, word, ID):
    word_positions = []

    if word in index_file:
        postings = index_file[word] #this should be a node object


        #begin loop----------------------------------------------------------
        count = 0
        while count < 5 or postings.get_node() != None:
            if postings.get_id() == ID: #Document ID must match before we can proceed
                #word_positions += postings.get_position()
                word_positions.extend(postings.get_position())

            postings.next()
            count += 1
        #end loop----------------------------------------------------------
        postings.reset()

        if len(word_positions) == 0: #didn't find anything?  return None
            return None
        return word_positions
    return None

#•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

def query_match(index_file: dict, phrase: [str], ID: int) -> int:
    inspected_words = [] #this prevents over-weighing the same terms
    score = 0

    #queries = phrase.split(" ")
    if len(phrase) > 1:
        #begin word-by-word process----------------------------------------------------------
        for a in range(1, len(phrase)):
            front_of_pair = phrase[a] #word in the front
    #         print("front: " + front_of_pair)
            back_of_pair = phrase[a-1] #word preceding front_of_pair
    #         print("back: " + back_of_pair)
    
            inspected_pair = (back_of_pair, front_of_pair) #I'll use this pair later
            front_word_positions = store_positions(index_file, front_of_pair, ID)
            back_word_positions = store_positions(index_file, back_of_pair, ID)
    
            #begin comparison for positions--------------------------------------------------
            if not ((inspected_pair in inspected_words) or ((inspected_pair[1], inspected_pair[0]) in inspected_words)):
                if not (front_word_positions is None or back_word_positions is None):
                    #[1, 3] #first word
                    #[2] #second word
                    for first_word_position in front_word_positions:
                        for second_word_position in back_word_positions:
    
    #                         if abs(first_word_position - second_word_position) == 4:
    #                             score += 2
    #                         elif abs(first_word_position - second_word_position) == 3:
    #                             score += 3
    #                         elif abs(first_word_position - second_word_position) == 2:
    #                             score += 4
                            if abs(first_word_position - second_word_position) == 1:
                                score += 5
                                if not ((inspected_pair in inspected_words) or ((inspected_pair[1], inspected_pair[0]) in inspected_words)):
                                    inspected_words.append(inspected_pair)
            #end comparison for positions-----------------------------------------------------
    #         print(inspected_words)
        #end word-by-word process-------------------------------------------------------------
    elif len(phrase) == 1 and (phrase[0] in index_file):
        score += 5
    return score

def tf_idf (index_file: dict, weighted_tf: int, word: str) -> int:
    '''gives term freq weighting * inverse doc freq weighting, 
    should only work for queries 2-terms and longer'''
    doc_freq = 0
#     print("index_file keys: ", index_file.keys())
    
    if word in index_file:
        doc_freq = index_file[word].length()
#         print("doc_freq: ", doc_freq)
#     print("index_file[word] score: ", index_file[word].get_score())
    tf = index_file[word].get_score() * weighted_tf
    print("tf: ", tf)
    idf = 55392/doc_freq
    print("idf: ", idf)
    new_score = 1+ log10(tf) * log10(idf)
    return new_score


if __name__ == '__main__':
    acm = Postings(1,10,[7])
#     acm2 = Postings(2, 1000, [22, 44]) 
    acm.add(2, 1000, [22, 44])
    test_output = {"ACM": acm}
    
    score = query_match(test_output, "ACM", 10)
    print("Sample phrase: ACM")
    print("Expected score: 5 | Actual score:", score, "\n")
    tfidf = tf_idf(test_output, score, "ACM")
    print("tf-idf : ", tfidf, "\n")
    
    #to
    post1 = Postings(1, 1, [41])
    post1.add(1, 1, [45])

    #be
    post2 = Postings(1, 1, [42])
    post2.add(1, 1, [46])

    #or
    post3 = Postings(1, 1, [43])

    #not
    post4 = Postings(1, 1, [44])

    index_output = {
        "to": post1,
        "be": post2,
        "or": post3,
        "not": post4,}
    
    score = query_match(index_output, "to be or not to be", 1)
    print("Sample phrase: to be or not to be")
    print("Expected score: 25 | Actual score:", score, "\n")

    #•••••••••••••••••••••••••••••••••••••

    #time
    post5 = Postings(1, 2, [1, 3])

    #to
    post6 = Postings(1, 2, [2])
    index_output2 = {
        "time": post5,
        "to": post6}

    score = query_match(index_output2, "time to time", 2)
    print("Repeated queries get a higher score; I can\'t solve this problem:")
    print("Update: solved")
    print("Expected score: 10 | Actual score:", score, "\n")

    #•••••••••••••••••••••••••••••••••••••

    #lol
    post6 = Postings(1, 3, [1, 4])

    #u
    post7 = Postings(1, 3, [2])

    #w0t
    post8 = Postings(1, 3, [3])

    index_output3 = {
        "lol": post6,
        "u": post7,
        "w0t": post8}

    score = query_match(index_output3, "lol u w0t", 2)
    print("Wrong ID\'s should return 0:")
    print("Expected score: 0 | Actual score:", score, "\n")

    #•••••••••••••••••••••••••••••••••••••

    #New
    postf = Postings(1, 444, [444])

    #York
    postm = Postings(1, 444, [445])

    #City
    postl = Postings(1, 444, [446])

    index_output4 = {
        "New": postf,
        "York": postm,
        "City": postl}

    score = query_match(index_output4, "New York City", 444)
    print("No repeated queries or terms")
    print("Expected score: 10 | Actual score:", score, "\n")

    #•••••••••••••••••••••••••••••••••••••

    #Δεν
    postden = Postings(1, 3, [1])

    #μπορώ
    postboro = Postings(1, 3, [2])

    #να
    postna = Postings(1, 3, [3])

    #το
    postto = Postings(1, 3, [4])

    #κάνω
    postkano = Postings(1, 3, [5])

    index_outputgr = {
        "Δεν": postden,
        "μπορώ": postboro,
        "να": postna,
        "το": postto,
        "κάνω": postkano}

    score = query_match(index_outputgr, "Δεν μπορώ να τη δω", 3)
    print("Testing random foreign characters:")
    print("Not all terms will match; this will return a lower score than maximum:")
    print("Expected score: 10 | Actual score:", score, "\n")

    #•••••••••••••••••••••••••••••••••••••

    score = query_match(index_output, "to match or maybe it won\'t", 1)
    print("Sample phrase: to be or not to be")
    print("No matches should return 0")
    print("Expected score: 0 | Actual score:", score, "\n")