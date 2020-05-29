
import time
from LL import Postings



def merge_index() -> None:
    """Deal with file managment. Input how many files you want to take in.
    It will always output 5 files."""
    with open("output_indexer0.txt", "r", encoding = 'utf8') as f0, \
         open("output_indexer1.txt", "r", encoding = 'utf8') as f1, \
         open("output_indexer2.txt", "r", encoding = 'utf8') as f2, \
         open("output_indexer3.txt", "r", encoding = 'utf8') as f3, \
         open("output_indexer4.txt", "r", encoding = 'utf8') as f4, \
         open("output_indexer5.txt", "r", encoding = 'utf8') as f5, \
         open("output_indexer6.txt", "r", encoding = 'utf8') as f6, \
         open("output_indexer7.txt", "r", encoding = 'utf8') as f7, \
         open("output_indexer8.txt", "r", encoding = 'utf8') as f8, \
         open("output_indexer9.txt", "r", encoding = 'utf8') as f9, \
         open("output_indexer10.txt", "r", encoding = 'utf8') as f10, \
         open("output_indexer11.txt", "r", encoding = 'utf8') as f11, \
         open("0-9_output_indexer.txt", "w", encoding = 'utf8') as w0, \
         open("A-F_output_indexer.txt", "w", encoding = 'utf8') as w1, \
         open("G-M_output_indexer.txt", "w", encoding = 'utf8') as w2, \
         open("N-S_output_indexer.txt", "w", encoding = 'utf8') as w3, \
         open("T-Z_output_indexer.txt", "w", encoding = 'utf8') as w4:
        files= [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]
        write= [w0, w1, w2, w3, w4]
        all_buffers= [add_buffer(f) for f in files]
        merging(all_buffers, write)


def add_buffer(open_file: 'file_object') -> [('token', 'Posting')]:
    """Load the next n lines into a file. Then convert them into postings"""
    count= 0
    total= []
    for line in open_file:
        total.append(line)
        count+= 1
        if count >= 500:    # Size of the buffer
            yield create_reading_buffer(total)
            total= []
            count= 0
    yield create_reading_buffer(total)  # Get remaining buffers
    yield None      # Empty


def create_reading_buffer(total:['str']) -> [('token', 'Posting')]:
    """It gets a buffer and converts it into a posting"""
    buffer= []
    for line in total:
        line= line.split("\t")
        post= add_posting(line)
        buffer.append((line[0].lower(), post))
    return buffer

def new_posting(line:[str]) -> "Postings":
    itemized_line = []
    for n in range(2,len(line)):
        node = line[n].strip(" -> ")
        itemized_line.append(node)
        if n == 100:
            break
    last= eval(itemized_line[0]) 
    post= Postings(last[0], last[1], last[2])
    if len(itemized_line) > 1:
        for i in range(-2, -len(itemized_line) - 1, -1):
            p= eval(itemized_line[i])
            post.add(p[0], p[1], p[2])
    return post

def add_posting(line:[str]) -> "Postings":
    line[2]= [i.strip() for i in line[2].split("->") if len(i) > 1]
    last= eval(line[2][-1])
    post= Postings(last[0], last[1], last[2])
    if len(line[2]) > 1:
        for i in range(-2, -len(line[2]) - 1, -1):
            p= eval(line[2][i])
            post.add(p[0], p[1], p[2])
    return post


def merging(r_files: ['generator'], w_files:['file_object']) -> None:
    """It iterates through previous indexes so it can create a couple of new
    indexes in alphabetical order. This way all the "a" indexes are in the
    same file"""
    tokens_post= [next(line) for line in r_files]
    # [[('token', 'Posting')]] with each list representing a file
    #[[('0', Postings), ('0..100.', Postings)],
    # [('0', Postings), ('0.01', Postings)] ]
    letters= ["0-9", "a-f", "g-m", "n-s", "t-z", "{"]
    buffer_writing= []
    count= 0
    n= 0 
    while len(r_files) > 0:
        word, similar_index= same_word([file[0][0] for file in tokens_post])
        if word == "{":
            break
        
        if 1 >= len(similar_index):
            post_line= single_match(tokens_post, r_files, similar_index[0])
        else:
            post_line= multiple_match(tokens_post, r_files, similar_index)

        if word[0] > letters[0][-1]:    # If the letter of current token is different,
            w_files.pop(0)              # then go to the next letter
            letters.pop(0)
            
        buffer_writing.append((word, post_line))
        count+= 1
        n+= 1
        
        if count > 1000:
            write_postings(buffer_writing, w_files[0])
            buffer_writing= []
            count= 0
            print(n)    # Checks merging progress
    write_postings(buffer_writing, w_files[0])


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


def single_match(tokens_post:[[('tokens', 'Postings')]], r_files: ['file_objects'], n:int) -> 'Postings':
    """It will return the posting. If the inner list is empty, it will get more tokens
    and postings. If it cannot get anymore, then it will remove that index from the
    list of token_post and files"""
    post_line= tokens_post[n][0][1]
    del tokens_post[n][0]
    if 1 > len(tokens_post[n]):
        next_batch= next(r_files[n])
        if next_batch == None:
            del tokens_post[n]
            del r_files[n]
        else:
            tokens_post[n]= next_batch
    return post_line


def multiple_match(tokens_post:[[('tokens', 'Postings')]], r_files: ['file_objects'], indexes:[int]) -> "Postings":
    n= indexes[0]
    post_line= tokens_post[n][0][1]
    for i in range(1, len(indexes)):    # Combines postings
        n= indexes[i]
        post_line.combine(tokens_post[n][0][1])

    for i in range(len(indexes) - 1, -1, -1):   # Solves the problem of removing indexing changes index
        n= indexes[i]
        del tokens_post[n][0]
        if 1 > len(tokens_post[n]):
            next_batch= next(r_files[n])
            if next_batch == None:
                del tokens_post[n]
                del r_files[n]
            else:
                tokens_post[n]= next_batch
    return post_line


def write_postings(buffer:[('token', 'Posting')], f:['file_object']) -> None:
    """Write the entire buffer into the given text file"""
    for line in buffer:
        line[1].reset()
        f.write(line[0].strip() + "\t" + str(line[1].counter()).strip() + "\t")
        while line[1].finish_iterating() == False:
            f.write(" -> " + str(line[1].get_node()).strip() + "\t")
            line[1].next()
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
                    #if letter == 'c':
                    #    char_number+= 1
                    t0.append(char_number)
                    w.write(letter + "\t" + str(char_number) + "\n")
                    lst.pop(0)

                char_number += len(line) + 1
            t.append(t0)
        
        print(t)
        for f, tt in zip(files, t):
            for num in tt:
                f.seek(num)
                line= f.readline()
                print(line[:40])
            print()
        




if __name__ == '__main__':
    start= time.time()
    #merge_index()  #Merging

    # Can't do this until you fix the merge list
    seek()     # Find position of the letters in different files
    end= time.time()
    print("Time", (end - start)/60, "minutes")




