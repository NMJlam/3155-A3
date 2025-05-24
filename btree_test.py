import random
import unittest 
from btree import Btree

def collectBTreeElems(root, res):
    '''
    Compiles the tree into a list using DFS
    '''

    if root.isLeaf(): 
        res += root.elements 
        return 

    for child in sorted(root.subtrees): 
        collectBTreeElems(child, res)

    return res 
    

class testBtreeInvariants(unittest.TestCase): 
    '''
    if the bound is 2 then we have max capacities of: 
    1) elements 2t-1
    2) subtrees 2t 
    for the lower bound: 
        - Non-root nodes must have t subtrees and t-1 elements
        - root node with >=1 elements is considered non-empty
    '''

    def test_lowerbound(self):
        pass 
    def test_upperbound(self): 
        pass 

class testInsertion(unittest.TestCase): 

    def test_basic_insertion(self): 
        '''
        Inserting directly into root node 
        Can insert up to the max elements 
        '''
        random.seed(88)
        # make random t values from 2-50
        tValues = [random.randint(2,50) for _ in range(10)] 

        for t in tValues: 
            max_elements = 2*t-1
            nums = random.sample(range(1, 1000000000), random.randint(1,max_elements-1)) 
            b = Btree(t)

            for num in nums:
                b.insert(num)

            with self.subTest(t=t): 
                self.assertTrue(b.root.isLeaf())
                self.assertEqual(sorted(nums), sorted(b.root.elements))

    def test_root_insertion(self): 
        '''
        Inserting and then breaking the root node
        '''
        random.seed(88)
        tValues = [random.randint(2,50) for _ in range(1)] 

        for t in tValues:
            max_elements = 2*t-1
            nums = random.sample(range(1,1000000000), max_elements+1)
            b = Btree(t)

            for num in nums: 
                b.insert(num)

            # perform checks: 
            with self.subTest(t=t): 
                self.assertFalse(b.root.isLeaf(), "Root should not be a leaf after split")
                self.assertEqual(len(b.root.elements), 1, "Root should contain 1 promoted median")
                self.assertEqual(len(b.root.subtrees), 2, "Root should have 2 children after split")

    def test_leaf_insertion(self):
        '''
        Inserting into a root node 
        '''
        pass 

if __name__ == '__main__': 
    unittest.main()








