






class LL:
    def __init__(self, value, next= None):
        self.value= value
        self.next= next




class LL_all:
    def __init__(self, values:[int]):
        """The value is a sorted list of ids. Make sure they are
        already sorted."""
        
        head= self.__initial_add(values)
        self.head= head         # The first node in the linked list
        self.current= head      # The current location


    @staticmethod
    def __initial_add(values:[int]):
        # Don't use this one
        front= end= LL(values[0])
        for v in values[1:]:
            end.next= LL(v)
            end= end.next
        return front



    def add(self, value:int):
        # Test case at the beginning, middle, end
        # Empty LL
        # Multiple adds
        if self.head == None:
            print(value)
            self.head= LL(value)
            self.current= self.head
            # I only change current bc it originally pointing to head
            # which it needs to update to the next head
            return

        ll= self.head

        if ll.value > value:
            self.head = LL(value, self.head)
            self.current= self.head
            return
        # Maybe combine this with above with something like
        # if (self.head == None) or (self.head.value > value):
        if ll.value == value:
            return
        

        ll= self.head
        ll_next= self.head.next

        while ll_next != None:
            if value < ll_next.value:
                new_LL= LL(value, ll_next)
                ll.next= new_LL
                return
            
            elif value == ll_next.value:
                return
             
            ll= ll_next
            ll_next= ll_next.next

        
        ll.next= LL(value)
        


    def add_list_values(self, values: [int]):
        pass



    def remove(self, value: int):
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

        
        












    def remove_list_values(self, values:[int]):
        pass



    def length(self):
        """Length of the entire LL, number of nodes"""
        count= 0
        ll= self.head
        while ll != None:
            count += 1
            ll= ll.next
        return count
    
    
    def value(self):
        if self.current == None:
            return None
        else:
            return self.current.value


    def next(self):
        """It doesn't return anything. It just updates current"""
        if self.current != None:
            self.current= self.current.next

    
    def reset(self):
        """If you previously iterated through the LL, this will reset it."""
        self.current= self.head
    

    def LL_to_list(self):
        ll= self.head
        values= []
        while ll != None:
            values.append(ll.value)
            ll= ll.next
        return values
    
    
    def index(self):
        """Value is in index"""
        pass






"""
postings= LL_all([1, 3, 5])

print("Length is", postings.length())
print()

print("LL to list", postings.LL_to_list())
print()

print("Current Value", postings.value())
print()


postings.next()
print("Current Value", postings.value())
print()



postings.add(4)


postings.next()
print("Current Value", postings.value())
print()


postings.add(6)
print("LL to list", postings.LL_to_list())
"""


















