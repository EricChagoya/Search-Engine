




from LL import LL_all
import unittest




class Test_LL(unittest.TestCase):

    def setUp(self):
        self.LL= LL_all([1, 3, 5, 7, 9])
        

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
        
    
    """
    def test_add_empty_LL(self):
        pass
    
    
    def test_add_list(self):
        pass
    """
    
    
    def test_remove(self):
        self.LL.remove(3)
        self.LL.remove(1)
        self.LL.remove(9)
        self.assertEqual([5, 7], self.LL.LL_to_list(), 
                         "Removing duplicates from the beginning, middle, and end")
    
    
    
    
    """
    def test_remove_list(self):
        pass
    
    """
    
    def test_multiple_add_remove(self):
        self.LL.add(8)
        self.LL.remove(1)
        self.LL.remove(2)
        self.LL.remove(4)
        self.LL.add(4)
        self.LL.remove(8)
        #print(self.LL.LL_to_list())
        self.assertEqual([3, 4, 5, 7, 9], self.LL.LL_to_list(), 
                         "Multiple Adding and Removing")
    
    
    
    def test_length(self):
        print(self.LL.LL_to_list() )
        self.assertCountEqual([1, 3, 5, 7, 9], self.LL.LL_to_list(), "Length is the same")
    
    
    
    
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
    
    
    """
    def test_reset(self):
        pass

    
    
    def test_insert_while_iterating(self):
        pass

    """





if __name__ == "__main__":
    unittest.main()

























