import random 
from classes.Btree_revised import BTree
from typing import List
from classes.node import Node 

class Commands(BTree): 

    def __init__(self, t): 
        super().__init__(t)

    def insertKeys(self, keys_to_insert: List[int]) -> None: 
        for key in keys_to_insert:
            self.insert(key)

    def deleteKeys(self, keys_to_delete: List[int]) -> None: 
        for key in keys_to_delete:
            self.delete(key)
   
    def select(self, n:int) -> int: 

        def kth_smallest(root: 'Node', k: int) -> int | None:
            if root is None or k < 0 or k >= root.count:
                return None
            
            for i in range(root.num_keys()):
                if not root.is_leaf() and i < root.num_children():
                    left_count = root.children[i].count
                    
                    if k < left_count:
                        return kth_smallest(root.children[i], k)
                    
                    k -= left_count
                
                if k == 0:
                    return root.keys[i]
                
                k -= 1
            
            if not root.is_leaf() and root.num_children() > root.num_keys():
                return kth_smallest(root.children[-1], k)
            
            return None

        res = kth_smallest(self.root, n-1) 
        return res if res else -1 

    def rank(self, num:int)-> int:

        def find_rank(node: 'Node', num: int, accumulated_rank: int) -> int:
            idx = node.search(num)
            
            current_rank = accumulated_rank
            
            if not node.is_leaf():
                for i in range(idx):
                    current_rank += node.children[i].count
            
            if idx < node.num_keys() and node.keys[idx] == num:
                if not node.is_leaf() and idx < node.num_children():
                    current_rank += node.children[idx].count
                return current_rank + idx
            
            if node.is_leaf():
                return -1
            
            current_rank += idx
            
            if idx < node.num_children():
                return find_rank(node.children[idx], num, current_rank)
            
            return -1        

        res = find_rank(self.root, num, 0)
        result = res + 1 if res != -1 else -1
        return result 
        
    def keysInRange(self, lower_bound:int, upper_bound:int) -> List[int]:

        def traverse(curr: 'Node', lower_bound: int, upper_bound: int, res: List[int])-> None:  

            i = 0 
            while i < curr.num_keys() and curr.keys[i] < lower_bound: 
                i += 1 

            if not curr.is_leaf() and i < curr.num_children(): 
                traverse(curr.children[i], lower_bound, upper_bound, res)

            while i < curr.num_keys() and curr.keys[i] <= upper_bound:
                
                if curr.keys[i] >= lower_bound:
                    res.append(curr.keys[i])
                if not curr.is_leaf() and i+1 < curr.num_children(): 
                    traverse(curr.children[i+1], lower_bound, upper_bound, res)
                i += 1

        res = [] 
        traverse(self.root, lower_bound, upper_bound, res)
        
        if not res: 
            return [-1]
        else: 
            return res 
    
    def primesInRange(self, lower_bound:int, upper_bound:int) -> List[int]:

        def miller_rabin(n): 
            if n < 2: 
                return False 
            if n == 2 or n ==3: 
                return True 
            if n < 2 or n % 2 ==0: 
                return False 

            r, s = 0, n-1 

            while s%2 == 0: 
                r += 1 
                s //= 2 

            for _ in range(10): 

                a = random.randrange(2, n-1)
                x = pow(a,s,n)

                if x == 1: 
                    continue 
                if x == n-1: 
                    continue 

                for _ in range(r-1): 
                    x = pow(x,2,n)
                    if x == n-1:
                        break 
                else: 
                    return False 

            return True 
        
        keys_in_range = self.keysInRange(lower_bound, upper_bound)

        if keys_in_range == [-1]: 
            return [-1]

        primes = [key for key in keys_in_range if miller_rabin(key)]

        return primes if primes else [-1]


if __name__ == '__main__':

    insertions = [
     12739121,
     58219403,
     45620117,
     10018273,
     34567890,
     98765432,
     123456789,
     10000019,
     999983,
     50000000,
     43219876,
     87654321,
     100000007,
     9999999967,
     76543210,
     314159265,
     271828183,
     99999959,
     88888888,
     1234567890
    ]

    c = Commands(35)
    c.insertKeys(insertions)
    
    deletions =  [
     99999959,
     88888888,
     1234567,
     98765432,
     50000000,
     58219403
    ]

    c.deleteKeys(deletions)

    print(c.primesInRange(1,100))
    print(c.keysInRange(50000000, 100000000))
    print(c.select(7))
    print(c.select(16))
    print(c.rank(1234567890))
    print(c.primesInRange(1,12345678))
    print(c.keysInRange(1,10))
    print(c.rank(42))


