import tkinter
import ranker
from LL import Postings
import search
import Indexer

def valid_query(user_input):
    '''Checks to see whether the query is:
    1) English/Roman characters
    2) Has no extra whitespace
    3) Not an empty input'''
    words = [term for term in user_input.get().split() if len(term) > 0]

    if len(words) < 1:
        return False

    for term in words:
        try:
            term.encode("utf-8").decode("ascii")
        except:
            return False
        words[words.index(term)] = Indexer.tokenizer(term.strip())
    return words

def interface(partial_index, ids, seeker, num_display):
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

    def display_results():
        '''This is a process that will display search results once the user has entered a query'''
        search_queries = valid_query(user_input) #list

        if search_queries == False:
            result_widget.config(text = "Not a valid search query; try again.")
            return

        proper_query = " "
        proper_query = proper_query.join(search_queries)
        result_widget.config(text = "Searching for " + proper_query)
        drawingspace.create_window(520, 300, window = result_widget)

        #Let's get the websites we should display now
        ranked = search.searching(partial_index, ids, seeker, num_display, search_queries)
        print(len(ranked))
        #PLAN A of displaying websites in the list-----------------------------------------

        result1 = tkinter.Label(root, text = "", font = ("Courier New", 12))
        result2 = tkinter.Label(root, text = "", font = ("Courier New", 12))
        result3 = tkinter.Label(root, text = "", font = ("Courier New", 12))
        result4 = tkinter.Label(root, text = "", font = ("Courier New", 12))
        result5 = tkinter.Label(root, text = "", font = ("Courier New", 12))

        def give_urls(website_list, r1, r2, r3, r4, r5):
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

        def order_NEXT():
            '''By clicking the next_button, the user will see the next 5 results'''
            global results_index
            results_index += 5

            while results_index > len(ranked) - 1 or results_index % 5 != 0:
                    results_index -= 1

            give_urls(ranked, result1, result2, result3, result4, result5)

        def order_PREV():
            '''By clicking the back_button, the user will see the previous 5 results'''
            global results_index
            results_index -= 5
            print(results_index)
            if results_index < 0:
                results_index = 0
            give_urls(ranked, result1, result2, result3, result4, result5)

        order_NEXT()
        next_button = tkinter.Button(text = "->", command = order_NEXT, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(560, 800, window=next_button)
        back_button = tkinter.Button(text = "<-", command = order_PREV, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(470, 800, window=back_button)

        return

    search_button = tkinter.Button(text = "Search", command = display_results, font = ("Comic Sans MS", 16, "bold"))
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
#extra notes:
#logn
#take note of idf score
#n = total number of documents
#dfi = amount of documents that contain a specific term

#**********************Display - High priority:
#ranked order: names of the websites list strings (already sorted)  
#num_display = 5

#**********************def valid_query() - High priority: It's... kinda done ;D
#loop until user enters a valid query
#English characters
#rules: remove leading/trailing whitespaces
#call tokenizer(string) -> returns one token at a time
#return of strings = [] every index has its own word

#Bonus: Index anchorwords for targeted pages.
#given: Use the .json file
#get the URL
#get the fragments
#return 1 result per .json
#return: dictionary = {key: words that are split | frequency: amount of times that the word appears in the URL}

#we only have 4 terms to look up
#this whole process will take a ton of hours to complete
#multiple search query example: meachine learning
#1) look up "machine"
#2) copy and paste the first 3 nodes into a .txt file
#combine scores if both terms are in the same ID
#3) look up "learning"
#4) copy and past the first 3 nodes into a .txt file
#5) do this for ALL output_indexer.txt
#6) add up ALL the scores if "machine" and "learning" are in the same doc ID
#7) We need five txt documents

#document frequency = number of documents which a token appears.
#ex: if you see "zine 2", the word "zine" appears in 2 documents