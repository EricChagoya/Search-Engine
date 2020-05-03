
from LL import LL_all
import unittest




class Test_LL(unittest.TestCase):

    def setUp(self):
        self.LL= LL_all([1, 3, 5, 7, 9])
    
    
    def test_empty_initialize_LL(self):
        ll= LL_all()
        self.assertEqual([], ll.LL_to_list(), "Empty LL has no contents")
        self.assertEqual(0, ll.length(), "Empty LL has size 0")
        

    def test_add(self):
        self.LL.add(4)      # Add to the middle
        self.LL.add(8)      # Add to the middle
        self.LL.add(10)     # Add to the end
        self.LL.add(11)     # Add to the middle
        self.LL.add(0)      # Add to the beginning
        self.LL.add(-1)      # Add to the beginning
        self.assertEqual([-1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11], self.LL.LL_to_list(), 
                         "Adding to the beginning, middle, and end")
    
    def test_add_duplicate(self):
        self.LL.add(3)
        self.LL.add(1)
        self.LL.add(9)
        self.LL.add(0)
        self.assertEqual([0, 1, 3, 5, 7, 9], self.LL.LL_to_list(), 
                         "Adding duplicates doesn't add to the LL")
    
    
    def test_add_list(self):
        values= [2, 6, 0, 4, 10]
        self.LL.add_list_values
        self.LL.add_list_values(values)
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 9, 10], self.LL.LL_to_list(), 
                         "Adding a list of numbers")
        #print(self.LL.LL_to_list())
        
    
    def test_remove(self):
        self.LL.remove(3)
        self.LL.remove(1)
        self.LL.remove(9)
        self.assertEqual([5, 7], self.LL.LL_to_list(), 
                         "Removing duplicates from the beginning, middle, and end")
        #print(self.LL.LL_to_list())
    

    def test_remove_list(self):
        values= [1, 5, 9]
        self.LL.remove_list_values(values)
        self.assertEqual([3, 7], self.LL.LL_to_list(), 
                         "Removing a list of numbers")
        #print(self.LL.LL_to_list())
    
    
    def test_multiple_add_remove(self):
        self.LL.add(8)
        self.LL.remove(1)
        self.LL.remove(2)
        self.LL.remove(4)
        self.LL.add(4)
        self.LL.remove(8)
        self.assertEqual([3, 4, 5, 7, 9], self.LL.LL_to_list(), 
                         "Multiple Adding and Removing has same content")
        self.assertEqual(len([3, 4, 5, 7, 9]), self.LL.length(), 
                         "Multiple Adding and Removing has same length")
        #print(self.LL.LL_to_list())
        
    
    def test_empty_LL(self):
        ll= LL_all([2])
        ll.remove(2)
        self.assertEqual([], ll.LL_to_list(), "Empty LL")
        self.assertEqual(None, ll.value(), "Empty LL produces None")
        
        ll.add(4)
        ll.add(3)
        ll.add(5)
        self.assertEqual([3, 4, 5], ll.LL_to_list(), "Add to empty LL")
        #print(self.LL.LL_to_list())
        
    
    def test_length(self):
        self.assertCountEqual([1, 3, 5, 7, 9], self.LL.LL_to_list(), "Length is the same")
        #print(self.LL.LL_to_list() )
    
    
    def test_value(self):
        self.assertEqual(1, self.LL.value())
        self.LL.next()
        self.assertEqual(3, self.LL.value())
        self.LL.next()
        self.assertEqual(5, self.LL.value())
        self.LL.next()
        self.assertEqual(7, self.LL.value())
        self.LL.next()
        self.assertEqual(9, self.LL.value())
        self.LL.next()
        self.assertEqual(None, self.LL.value())

    
    def test_next(self):
        """Once it stops iterating, the value will be None. If you call next on None Node,
        it still returns None."""
        self.LL.next()
        self.LL.next()
        self.LL.next()
        self.LL.next()
        self.LL.next()
        self.assertEqual(None, self.LL.value())
        self.LL.next()
        self.assertEqual(None, self.LL.value())
    
    
    def test_reset(self):
        self.assertEqual(1, self.LL.value())
        self.LL.next()
        self.assertEqual(3, self.LL.value())
        self.LL.next()
        self.assertEqual(5, self.LL.value())
        self.LL.next()
        self.assertEqual(7, self.LL.value())
        self.LL.next()
        self.assertEqual(9, self.LL.value())
        self.LL.next()
        self.assertEqual(None, self.LL.value())
        
        self.LL.reset()
        self.assertEqual(1, self.LL.value())
        self.LL.next()
        self.assertEqual(3, self.LL.value())
        
        self.LL.reset()
        self.assertEqual(1, self.LL.value())
    
    
    def test_index(self):
        self.assertEqual(self.LL.index(1), 0, "Index matches beginning")
        self.assertEqual(self.LL.index(5), 2, "Index matches middle")
        self.assertEqual(self.LL.index(9), 4, "Index matches end")
        self.assertEqual(self.LL.index(10), None, "Can't find index")
        
        self.LL.add(8)
        self.assertEqual(self.LL.index(9), 5, "Index matches end")
        
    
    def test_insert_remove_while_iterating(self):
        self.LL.next()
        self.LL.add(2)
        self.assertEqual(3, self.LL.value())
        self.assertEqual(6, self.LL.length())
        self.LL.add(4)
        self.LL.next()
        self.assertEqual(4, self.LL.value())
        
        self.LL.reset()
        self.assertEqual(1, self.LL.value())
        self.LL.next()
        self.assertEqual(2, self.LL.value())
        self.LL.next()
        self.LL.next()
        self.LL.remove(5)
        self.LL.remove(1)
        self.LL.next()
        self.assertEqual(7, self.LL.value())
        
        self.LL.reset()
        self.assertEqual(2, self.LL.value())
        #print(self.LL.LL_to_list())




if __name__ == "__main__":
    unittest.main()

























