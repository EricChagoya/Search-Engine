import time
import tkinter

import search
import Indexer
from LL import Postings

def valid_query(user_input: tkinter.Entry, result_widget: tkinter.Label)-> [str] or bool:
    '''Checks to see whether the query has English characters and not empty'''
    words = [term for term in user_input.get().split() if len(term) > 0]

    if len(words) < 1:
        return False

    valid_words = []
    for term in words:
        try:
            term.encode("utf-8").decode("ascii")
            valid_words.append(Indexer.tokenizer(term.strip()))
        except:
            print("There\'s an invalid query; skipping...")

    if 0 < len(valid_words):
        proper_query = " "
        proper_query = proper_query.join(valid_words)
        result_widget.config(text = "Searching for " + proper_query)
        return valid_words
    return False

def interface(partial_index: {str:'Postings'}, ids: {int:str}, seeker: {'letter':int},
              num_display: int, files:['file_object']) -> None  :
    '''Main function for the VISUALS of our search engine; most (or all) of the visuals in our
    program is defined by this function'''
    global results_index
    results_index = 0

    root = tkinter.Tk()

    drawingspace = tkinter.Canvas(root, width = 1000, height = 1000, relief = 'raised')
    drawingspace.pack()

    title = tkinter.Label(root, text = "Search the index", font = ("Impact", 44))
    drawingspace.create_window(510, 100, window=title)

    user_input = tkinter.Entry(root)
    result_widget = tkinter.Label(root,text = "", font = ("Courier New", 22))
    drawingspace.create_window(510, 200, window=user_input)

    result1 = tkinter.Label(root, text = "", font = ("Courier New", 12))
    result2 = tkinter.Label(root, text = "", font = ("Courier New", 12))
    result3 = tkinter.Label(root, text = "", font = ("Courier New", 12))
    result4 = tkinter.Label(root, text = "", font = ("Courier New", 12))
    result5 = tkinter.Label(root, text = "", font = ("Courier New", 12))

    #Define display_results() function•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

    def display_results(search_queries: list)->None:
        '''This is a process that will display search results once the user has entered a query'''

        drawingspace.create_window(520, 300, window = result_widget)

        start= time.time()
        ranked = search.searching(partial_index, ids, seeker, num_display, search_queries, files) #gets websites to display
        end= time.time()
        timer = (end - start) * 1000
        timer = "{:.0f}".format(timer)


        #Important: the list "ranked" is not used until the user presses the "->" or "<-" buttons

        #Define give_urls() function•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
        def give_urls(website_list: list, r1: tkinter.Label, r2: tkinter.Label, r3: tkinter.Label, r4: tkinter.Label, r5: tkinter.Label)-> None:
            '''Displays (with TKinter) five search results at a time'''
            global results_index

            try:
                r1.config(text = website_list[results_index])
                drawingspace.create_window(520, 450, window = r1)
            except:
                r1.config(text = "*************End of results*************")
                drawingspace.create_window(520, 450, window = r1)
                r2.config(text = "")
                drawingspace.create_window(520, 500, window = r2)
                r3.config(text = "")
                drawingspace.create_window(520, 550, window = r3)
                r4.config(text = "")
                drawingspace.create_window(520, 600, window = r4)
                r5.config(text = "")
                drawingspace.create_window(520, 650, window = r5)
                return
            try:
                r2.config(text = website_list[results_index+1])
                drawingspace.create_window(520, 500, window = r2)
            except:
                r2.config(text = "*************End of results*************")
                drawingspace.create_window(520, 500, window = r2)
                r3.config(text = "")
                drawingspace.create_window(520, 550, window = r3)
                r4.config(text = "")
                drawingspace.create_window(520, 600, window = r4)
                r5.config(text = "")
                drawingspace.create_window(520, 650, window = r5)
                return
            try:
                r3.config(text = website_list[results_index+2])
                drawingspace.create_window(520, 550, window = r3)
            except:
                r3.config(text = "*************End of results*************")
                drawingspace.create_window(520, 550, window = r3)
                r4.config(text = "")
                drawingspace.create_window(520, 600, window = r4)
                r5.config(text = "")
                drawingspace.create_window(520, 650, window = r5)
                return
            try:
                r4.config(text = website_list[results_index+3])
                drawingspace.create_window(520, 600, window = r4)
            except:
                r4.config(text = "*************End of results*************")
                drawingspace.create_window(520, 600, window = r4)
                r5.config(text = "")
                drawingspace.create_window(520, 650, window = r5)
                return
            try:
                r5.config(text = website_list[results_index+4])
                drawingspace.create_window(520, 650, window = r5)
            except:
                r5.config(text = "*************End of results*************")
                drawingspace.create_window(520, 650, window = r5)
                return

            return
        #End give_urls() function••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

        #These functions help display five results at a time•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
        def order_FIRST()->None:
            '''Display first results without clicking the "next_button" or "back_button"'''
            global results_index
            results_index = 0
            give_urls(ranked, result1, result2, result3, result4, result5)


        def order_NEXT()->None:
            '''By clicking the next_button, the user will see the next 5 results'''
            global results_index
            results_index += 5
            while results_index > len(ranked) - 1 or results_index % 5 != 0:
                    results_index -= 1
            give_urls(ranked, result1, result2, result3, result4, result5)


        def order_PREV()->None:
            '''By clicking the back_button, the user will see the previous 5 results'''
            global results_index
            results_index -= 5
            #print(results_index)
            if results_index < 0:
                results_index = 0
            give_urls(ranked, result1, result2, result3, result4, result5)
        #End of functions that display five results at a time••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

        order_FIRST()
        next_button = tkinter.Button(text = "->", command = order_NEXT, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(560, 800, window=next_button)
        back_button = tkinter.Button(text = "<-", command = order_PREV, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(470, 800, window=back_button)

        timerlabel = tkinter.Label(root, text = "Time: " + str(timer) + "ms", font = ("Courier New", 16, "bold"))
        drawingspace.create_window(510, 850, window=timerlabel)

        return
    #End display_results() function•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

    def process_query()->None:
        '''Validates a user's queries before attempting to activate the protocol to display the results'''

        search_queries = valid_query(user_input, result_widget)
        if search_queries != False:
            display_results(search_queries)

        else: #I know this "else" statement may be redundant, but a bug occurs without this statement for some reason
        #this bug causes the program to present results in the list "ranked" despite an invalid input
            result_widget.config(text = "Invalid query")
            result1.config(text = "")
            result2.config(text = "")
            result3.config(text = "")
            result4.config(text = "")
            result5.config(text = "")

    search_button = tkinter.Button(text = "Search", command = process_query, font = ("Comic Sans MS", 16, "bold"))
    drawingspace.create_window(510, 240, window=search_button)
    root.mainloop()



if __name__ == '__main__':
    partial_index= dict()
    ids= search.get_ids()
    seeker= search.seek_dict()
    num_display= 5
    
    post1 = Postings(1, 1, [41])    #to
    post1.add(1, 1, [45])
    post1.add(1, 2, [32])

    post2 = Postings(1, 1, [42])    #be
    post2.add(1, 1, [46])
    post2.add(1, 2, [33])

    post3 = Postings(1, 1, [43])    #or

    post4 = Postings(1, 1, [44])    #not

    index_output = {"to": post1, "be": post2, "or": post3, "not": post4}


    with open("0-9_output_indexer.txt", "r", encoding = 'utf8') as f0, \
         open("A-F_output_indexer.txt", "r", encoding = 'utf8') as f1, \
         open("G-M_output_indexer.txt", "r", encoding = 'utf8') as f2, \
         open("N-S_output_indexer.txt", "r", encoding = 'utf8') as f3, \
         open("T-Z_output_indexer.txt", "r", encoding = 'utf8') as f4:
        files= [f0, f1, f2, f3, f4]
        interface(partial_index, ids, seeker, num_display, files)
    print("end")










