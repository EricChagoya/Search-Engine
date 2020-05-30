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

    if len(phrase) > 1:
        #begin word-by-word process----------------------------------------------------------
        for a in range(1, len(phrase)):
            front_of_pair = phrase[a] #word in the front
            back_of_pair = phrase[a-1] #word preceding front_of_pair
    
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
                            if abs(first_word_position - second_word_position) == 1:
                                score += 5
                                if not ((inspected_pair in inspected_words) or ((inspected_pair[1], inspected_pair[0]) in inspected_words)):
                                    inspected_words.append(inspected_pair)
            #end comparison for positions-----------------------------------------------------
        #end word-by-word process-------------------------------------------------------------
    elif len(phrase) == 1 and (phrase[0] in index_file):
        score += 5
    return score
    
 
