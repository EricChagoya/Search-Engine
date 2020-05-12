

class LL:
    """Don't use this class. This class is used by LL_all."""
    def __init__(self, score: int, ids:int, position:[int], next= None):
        self.score= score
        self.ids= ids
        self.position= position
        self.next= next
        

class Postings:
    def __init__(self, score: int, ids: int, position: [int]) -> None:
        head= LL(score, ids, position)
        self.head= head         # The first node in the linked list
        self.current= head      # The current location while iterating
        self.count= 1           # Number of nodes in the LL
    
    
    def add(self, score: int, ids: int, position: [int]) -> None:
        """It sorts from highest score to lowest"""
        if (self.head == None) or (score > self.head.score):
            self.head = LL(score, ids, position, self.head)
            self.current = self.head
            self.count += 1
            return
        
        ll = self.head
        ll_next = self.head.next
        while ll_next != None:
            if score > ll_next.score:
                new_LL = LL(score, ids, position, ll_next)
                ll.next = new_LL
                self.count += 1
                return
            ll= ll_next
            ll_next= ll_next.next
        ll.next= LL(score, ids, position)
        self.count += 1
    
    
    def remove(self, ids:int) -> None:
        """Remove a node based off it's id"""
        if (self.head == None):
            raise Exception('Cannot remove id if LL is empty')
        
        if self.current.ids == ids:
            self.current= self.current.next
        
        if ids == self.head.ids:
            self.head= self.head.next
            self.count -= 1
            return
        
        ll= self.head
        ll_prev= None
        while ll != None:
            if ll.ids == ids:
                ll_prev.next= ll.next
                self.count -= 1
                return
            ll_prev= ll
            ll= ll.next
        raise Exception(f"Id {ids} does not exist")


    def next(self) -> None:
        """It doesn't return anything. It just updates current"""
        if self.current != None:
            self.current= self.current.next

    def finish_iterating(self):
        if self.current == None:
            return True
        return False

    def reset(self) -> None:
        """If you previously iterated through the LL, this will reset it."""
        self.current= self.head


    def combine(self, post2) -> None:
        """It combines two Postings and tries to order them from highest
        score to lowest. The Postings should already be sorted"""
        self.reset()
        post2.reset()
        new_post= Postings(999999999, -1, [0])
        
        while not self.finish_iterating() or not post2.finish_iterating():
            score1= self.get_score()
            score2= post2.get_score()
            
            if score1 == None:
                new_post.add(score2, post2.get_id(), post2.get_position())
                post2.next()
            elif score2 == None:
                new_post.add(score1, self.get_id(), self.get_position())
                self.next()
            else:
                if score1 < score2:
                    new_post.add(score2, post2.get_id(), post2.get_position())
                    post2.next()
                else:
                    new_post.add(score1, self.get_id(), self.get_position())
                    self.next()

        new_post.remove(-1)
        self.head= new_post.head
        self.current= self.head
        self.count= self.length()


    def counter(self) -> int:
        return self.count
    
    def length(self) -> int:
        """Length of the entire LL, number of nodes"""
        count= 0
        ll= self.head
        while ll != None:
            count += 1
            ll= ll.next
        self.count= count
        return count

    def get_node(self):
        """It returns a tuple of the score, id, and positions"""
        if self.current != None:
            return self.get_score(), self.get_id(), self.get_position()
    
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







# I have no mechanism where to see if that id already being used
# I'm not checking if a duplicate id is already inside











