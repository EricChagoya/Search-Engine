


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





# I"m probably going to delete this one
class LL_all:
    """This class will take care of the small details like knowing what the first value is, 
    add/remove values, change the head if the head has been removed or there is a value smaller
    then the current head."""
    
    def __init__(self, values= []) -> None:
        """The value is a sorted list of ids. Make sure they are
        already sorted."""
        head= self.__initial_add(values)
        self.head= head         # The first node in the linked list
        self.current= head      # The current location


    @staticmethod
    def __initial_add(values:[int]) -> "LL":
        # Don't use this method
        if len(values) == 0:
            return None
        front= end= LL(values[0])
        for v in values[1:]:
            end.next= LL(v)
            end= end.next
        return front


    def add(self, value:int) -> None:
        """Add an integer to the LL. It will make sure the value is sorted."""
        if (self.head == None) or (self.head.value > value):    # If LL is empty or value is less than the value
            self.head= LL(value, self.head)
            self.current= self.head
            return
        elif self.head.value == value:  # If value is the head of the LL
            return
        
        ll= self.head
        ll_next= self.head.next
        while ll_next != None:
            if value < ll_next.value:
                new_LL= LL(value, ll_next)
                ll.next= new_LL
                return
            elif value == ll_next.value:    # If value is already in LL
                return
            ll= ll_next
            ll_next= ll_next.next
        
        ll.next= LL(value)  # Add to the end
        

    def add_list_values(self, values: [int]) -> None:
        for v in values:
            self.add(v)


    def remove(self, value: int) -> None:
        if self.head ==None:    # Cannot remove from an empty LL
            return
        if value == self.head.value:     # Remove the first instance
            self.head= self.head.next
            return
            
        ll= self.head
        ll_prev= None
        while ll != None:
            if ll.value == value:
                ll_prev.next= ll.next
            ll_prev= ll
            ll= ll.next


    def remove_list_values(self, values:[int]) -> None:
        for v in values:
            self.remove(v)


    def length(self) -> int:
        """Length of the entire LL, number of nodes"""
        count= 0
        ll= self.head
        while ll != None:
            count += 1
            ll= ll.next
        return count
    
    
    def value(self) -> None or int:
        """Return the value of the current node"""
        if self.current == None or self.head == None:
            return None
        else:
            return self.current.value


    def next(self) -> None:
        """It doesn't return anything. It just updates current"""
        if self.current != None:
            self.current= self.current.next

    
    def reset(self) -> None:
        """If you previously iterated through the LL, this will reset it."""
        self.current= self.head
    

    def LL_to_list(self) -> [int]:
        """I mostly used this for testing purposes. I'm not sure if it should
        be used outside of that purpose."""
        ll= self.head
        values= []
        while ll != None:
            values.append(ll.value)
            ll= ll.next
        return values
    
    
    def index(self, value: int) -> int or None:
        """It tries to find the value in the LL. It returns what 
        position it is in. None otherwise."""
        count= 0
        ll= self.head
        while ll!= None:
            if ll.value == value:
                return count
            ll= ll.next
            count+= 1        
        return None





# I'm not throwing exceptions if you try to remove a value that isn't there
# or add a value that is already in the LL.
# I'm not sure if you guys want me to add that as an extra safety net when
# someone misuses the class.


# Throw an exception if trying to delete a node that doesn't exist


# I have no mechanism where to see if that id already being used.
# We can maybe implement similar documents before, like right after we tokenize but before indexing.
#We can use the function check_duplicates from the crawler 


# I'm not checking if a duplicate id is already inside











