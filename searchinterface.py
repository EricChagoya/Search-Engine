import tkinter
import ranker
from LL import Postings
import search
import Indexer

def valid_query(user_input: tkinter.Entry, result_widget: tkinter.Label)->list or bool:
    '''Checks to see whether the query is:
    1) English/Roman characters
    2) Has no extra whitespace
    3) Not an empty input'''
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

    if len(valid_words) > len(words) // 2:
        proper_query = " "
        proper_query = proper_query.join(valid_words)
        result_widget.config(text = "Searching for " + proper_query)
        return valid_words
        
    return False

def interface(partial_index: dict, ids: {int:str}, seeker: {'letter':int}, num_display: int) -> None  :
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

        ranked = search.searching(partial_index, ids, seeker, num_display, search_queries) #gets websites to display

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
            print(results_index)
            if results_index < 0:
                results_index = 0
            give_urls(ranked, result1, result2, result3, result4, result5)
        #End of functions that display five results at a time••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

        order_FIRST()
        next_button = tkinter.Button(text = "->", command = order_NEXT, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(560, 800, window=next_button)
        back_button = tkinter.Button(text = "<-", command = order_PREV, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(470, 800, window=back_button)

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
    #to
    post1 = Postings(1, 1, [41])
    post1.add(1, 1, [45])
    post1.add(1, 2, [32])

    #be
    post2 = Postings(1, 1, [42])
    post2.add(1, 1, [46])
    post2.add(1, 2, [33])

    #or
    post3 = Postings(1, 1, [43])

    #not
    post4 = Postings(1, 1, [44])

    index_output = {
        "to": post1,
        "be": post2,
        "or": post3,
        "not": post4,}
    a = interface(partial_index, ids, seeker, num_display)
    print(a)
    print("end")