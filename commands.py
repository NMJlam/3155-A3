import random 
from Btree_revised import BTree
from typing import List
from node import Node 

class commands(BTree): 

    def __init__(self, t): 
        super().__init__(t)

    def insert_keys(self, keys_to_insert: List[int]) -> None: 
        for key in keys_to_insert:
            self.insert_rec(key, self.root)

    def delete_keys(self, keys_to_delete: List[int]) -> None: 
        for key in keys_to_delete:
            self.delete(key)
    
    def select(self, num:int) -> int: 
        pass 

    def rank(self, num: int):
        
        def rec_search(root: 'Node', depth: int) -> int | None: 

            if root.contains(num): 
                return depth 

            elif root.is_leaf(): 
                return -1 
            
            idx = root.search(num)
            child = root.children[idx]
            depth += 1
            return rec_search(child, depth)
        
        return rec_search(self.root, 1)
    
    def keysInRange(self, lower_bound:int, upper_bound:int) -> List[int]:
        pass 
    
    def primesInRange(self, lower_bound:int, upper_bound:int) -> List[int]:
        pass 

if __name__ == '__main__':
    random.seed(88)
    insertions =  random.sample(range(0,100), 10)

    c = commands(3)
    c.insert_keys(insertions)
    print(c)
    print(c.rank(24))

