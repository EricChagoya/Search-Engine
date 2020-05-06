



class LL:
    """Don't use this class. This class is used by LL_all."""
    def __init__(self, score: int, ids:int, position:[int], next= None):
        #self.value= value
        self.score= score
        self.ids= ids
        self.position= position
        self.next= next
        

class Postings:
    def __init__(self, score: int, ids: int, position: [int]) -> None:
        head= LL(score, ids, position)
        self.head= head         # The first node in the linked list
        self.current= head      # The current location while iterating
    
    
    def add(self, score: int, ids: int, position: [int]) -> None:
        """It sorts from highest score to lowest"""
        if (self.head == None) or (score > self.head.score):
            self.head= LL(score, ids, position, self.head)
            self.current= self.head
            return
        
        ll= self.head
        ll_next= self.head.next
        while ll_next != None:
            if score > ll_next.score:
                new_LL= LL(score, ids, position, ll_next)
                ll.next= new_LL
                return
            ll= ll_next
            ll_next= ll_next.next
        ll.next= LL(score, ids, position)
    
    
    def remove(self, ids:int) -> None:
        """Remove a node based off it's id"""
        if (self.head == None):
            raise Exception('Cannot remove id if LL is empty')
        
        if self.current.ids == ids:
            self.current= self.current.next
        
        
        if ids == self.head.ids:
            self.head= self.head.next
            return
        
        ll= self.head
        ll_prev= None
        while ll != None:
            if ll.ids == ids:
                ll_prev.next= ll.next
                return
            ll_prev= ll
            ll= ll.next
        raise Exception(f"Id {ids} does not exist")
    
    
    def length(self) -> int:
        """Length of the entire LL, number of nodes"""
        count= 0
        ll= self.head
        while ll != None:
            count += 1
            ll= ll.next
        return count
    
    
    def get_score(self) -> None or int:
        """Return the value of the current node"""
        if self.current == None or self.head == None:
            return None
        else:
            return self.current.score
    
    
    def get_id(self) -> None or int:
        """Return the value of the current node"""
        if self.current == None or self.head == None:
            return None
        else:
            return self.current.ids
    
    def get_position(self) -> None or int:
        """Return the value of the current node"""
        if self.current == None or self.head == None:
            return None
        else:
            return self.current.position


    def next(self) -> None:
        """It doesn't return anything. It just updates current"""
        if self.current != None:
            self.current= self.current.next

    
    def reset(self) -> None:
        """If you previously iterated through the LL, this will reset it."""
        self.current= self.head
    
    
    def scores_to_list(self) -> int:
        """I mostly used this and the following two functions for testing purposes. 
        I'm not sure if it should be used outside of that purpose."""
        ll= self.head
        scores= []
        while ll != None:
            scores.append(ll.score)
            ll= ll.next
        return scores

    def ids_to_list(self) -> int:
        ll= self.head
        ids= []
        while ll != None:
            ids.append(ll.ids)
            ll= ll.next
        return ids

    def positions_to_list(self) -> int:
        ll= self.head
        positions= []
        while ll != None:
            positions.append(ll.position)
            ll= ll.next
        return positions

    def print_nodes(self) -> None:
        """It prints the nodes in the format score, id, then positions."""
        ll= self.head
        while ll != None:
            print("Score:", ll.score, end= '  ')
            print("ID:", ll.ids, end= '  ')
            print("Positions:", ll.position, end= '  ')
            print("->\t", end= "")

            
            ll= ll.next
        print("None")

    def get_node(self):
        if self.current != None:
            return self.get_score(), self.get_id(), self.get_position()


    def finish_iterating(self):
        if self.current == None:
            return True
        return False





# I have no mechanism where to see if that id already being used.
# We can maybe implement similar documents before, like right after we tokenize but before indexing.
#We can use the function check_duplicates from the crawler 


# I'm not checking if a duplicate id is already inside











