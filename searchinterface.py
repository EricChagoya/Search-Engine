import tkinter
import ranker
from LL import Postings
import search
import Indexer

def valid_query(user_input):
    #I tried to do some ICS 33-level stuff but there might be a test case that breaks this
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
    global current_results
    current_results = 0

    root = tkinter.Tk()

    drawingspace = tkinter.Canvas(root, width = 1000, height = 1000, relief = 'raised')
    drawingspace.pack()

    title = tkinter.Label(root, text = "Search the index", font = ("Impact", 44))
    drawingspace.create_window(510, 100, window=title)

    user_input = tkinter.Entry(root)
    result_widget = tkinter.Label(root,text = "", font = ("Courier New", 22))
    drawingspace.create_window(510, 200, window=user_input)

    def page_display_sites(website_list, order):
        if order < 0:
            return

        result1.config(text = website_list[order])
        drawingspace.create_window(510, 350, window=result1)
        result2.config(text = website_list[order+1])
        drawingspace.create_window(510, 400, window=result2)
        result3.config(text = website_list[order+2])
        drawingspace.create_window(510, 450, window=result3)
        result4.config(text = website_list[order+3])
        drawingspace.create_window(510, 500, window=result4)
        result5.config(text = website_list[order+4])
        drawingspace.create_window(510, 550, window=result5)
        return

    def display_results():
        search_queries = valid_query(user_input) #list

        if search_queries == False:
            result_widget.config(text = "Not a valid search query; try again.")
            return

        proper_query = " "
        proper_query = proper_query.join(search_queries)
        result_widget.config(text = "Searching for " + proper_query)
        drawingspace.create_window(520, 399, window = result_widget)

        #Let's get the websites we should display now
        ranked = search.searching(partial_index, ids, seeker, num_display, search_queries)
        #PLAN A of displaying websites in the list-----------------------------------------
        result1 = tkinter.Label(root, text = "", font = ("Courier New", 22))
        result2 = tkinter.Label(root, text = "", font = ("Courier New", 22))
        result3 = tkinter.Label(root, text = "", font = ("Courier New", 22))
        result4 = tkinter.Label(root, text = "", font = ("Courier New", 22))
        result5 = tkinter.Label(root, text = "", font = ("Courier New", 22))

        def order_NEXT():
            global current_results
            current_results += 5
            print(current_results)
            page_display_sites(ranked, current_results)
            return

        def order_PREV():
            global current_results
            if current_results <= 0:
                return
            current_results -= 5
            print(current_results)
            page_display_sites(ranked, current_results)
            return

        next_button = tkinter.Button(text = "Next", command = order_NEXT, font = ("Comic Sans MS", 16, "bold"))
        back_button = tkinter.Button(text = "Prev", command = order_PREV, font = ("Comic Sans MS", 16, "bold"))
        drawingspace.create_window(570, 800, window=next_button)
        drawingspace.create_window(480, 800, window=back_button)
        #end PLAN A------------------------------------------------------------------------


        #PLAN B of displaying websites in the list-----------------------------------------
        #vertical_coordinate = 349
        #for website in ranked:
            #result = tkinter.Label(root, text = str(website), font = ("Courier New", 22))
            #drawingspace.create_window(520, vertical_coordinate, window = result)
            #vertical_coordinate += 50
        #end PLAN B------------------------------------------------------------------------

        #partial_index["c"] = 3
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