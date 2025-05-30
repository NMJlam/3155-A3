import random
import unittest 
from classes.Btree_revised import BTree 
from classes.node import Node 

def test_count(root: 'Node') -> bool: 

    if root.is_leaf(): 
        return len(root.keys) == root.count 
    
    count = 0 

    for child in root.children: 
        test_count(child)
        count += child.count 

    return count + root.num_keys() == root.count

class test_bTree(unittest.TestCase):

    def test_count1000(self): 
        b = BTree(2)

        random.seed(88)
        insertions = random.sample( range(0,10000), 1000)

        for i in insertions: 
            b.insert(i)

        random.shuffle(insertions)

        count = 0 
        for i in insertions: 
            b.delete(i)
            result = test_count(b.root)
            if result == True: 
                count += 1 

        self.assertEqual(count, 1000)

    def test_count10000(self): 

        b = BTree(11)

        random.seed(100)

        insertions = random.sample(range(0,1000000000), 10000)

        for i in insertions: 
            b.insert(i)

        random.shuffle(insertions)

        count = 0 
        for i in insertions: 
            b.delete(i)
            res = test_count(b.root)
            if res == True: 
                count += 1 

        self.assertEqual(count, 10000)



if __name__ == "__main__": 
    unittest.main()

        




