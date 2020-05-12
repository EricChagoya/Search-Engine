import tkinter
import ranker
from LL import Postings

def pass_to_other_function(words, root, canvas):
    currentscore = (0, 0) #tuple format: (document_ID, query_match score)

    #This code will (should) be changed/deleted as we put all our tasks together
    for document_ID in range(0, 3):
        #print("Searched: ", document_ID)
        temporaryscore = ranker.query_match(index_output, words, document_ID)
        if temporaryscore > currentscore[1]:
            currentscore = (document_ID, temporaryscore)
    #---------------------------------------------------------------------------

    display_best = tkinter.Label(root, text = "Best document ID (based on matches): " + str(currentscore[0]), font = ("Berlin Sans FB", 22))
    canvas.create_window(500, 450, window = display_best)

def interface():

    root = tkinter.Tk()

    drawingspace = tkinter.Canvas(root, width = 1000, height = 500, relief = 'raised')
    drawingspace.pack()

    title = tkinter.Label(root, text = "Search the index", font = ("Impact", 44))
    drawingspace.create_window(510, 100, window=title)

    #subtitle = tkinter.Label(root, text = "this ain\'t google but who tf cares", font = ("Comic Sans MS", 12))
    #drawingspace.create_window(500, 175, window=subtitle)

    user_input = tkinter.Entry(root)
    drawingspace.create_window(510, 200, window=user_input)

    def display_results():
        search_queries = user_input.get()

        results = tkinter.Label(root, text = "Searching for " + search_queries, font = ("Courier New", 22))
        drawingspace.create_window(520, 399, window = results)

        #I'm passing root and drawingspace just because they're technically the
        #"print" statements for TKinter
        return pass_to_other_function(search_queries, root, drawingspace)

    search_button = tkinter.Button(text = "Search", command = display_results, font = ("Comic Sans", 16, "bold"))
    drawingspace.create_window(510, 240, window=search_button)

    root.mainloop()

if __name__ == '__main__':
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
    interface()