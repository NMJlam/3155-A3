import random 
from typing import Tuple, List
from typing import List
import sys

import classes.commands as commands 

class Node: 

    def __init__(self, keys: List[int], children: List['Node']) -> None: 
        self.keys = keys 
        self.children = children 
        self.count = 0
        self.recalculate_count()

    def num_keys(self) -> int: 
        return len(self.keys)

    def num_children(self) -> int: 
        return len(self.children)

    def is_leaf(self) -> bool: 
        return self.num_children() == 0 
    
    def recalculate_count(self) -> None: 
        if self.is_leaf(): 
            self.count = self.num_keys()
        else:
            self.count = self.num_keys() + sum(child.count for child in self.children)

    def search(self, target:int) -> int: 
        lo, hi = 0, self.num_keys() - 1
        while lo <= hi:
            mid = (lo+hi) // 2
            if target < self.keys[mid]:
                hi = mid-1
            elif target > self.keys[mid]:
                lo = mid+1 
            else: 
                return mid 
        return lo 
    
    def insert_node(self, num:int) -> None: 
        insertion_index = self.search(num)
        self.keys.insert(insertion_index, num)

    def split_child_at(self, index:int) -> None:

        child =  self.children[index]
        median = (child.num_keys()) // 2 
        median_element = child.keys[median]

        left = Node(child.keys[:median], child.children[:median+1])
        right = Node(child.keys[median+1:], child.children[median+1:])

        self.keys.insert(index, median_element)
        self.children[index:index+1] = [left,right]

        left.recalculate_count()
        right.recalculate_count()
        self.recalculate_count()

    def split_new_root(self): 
        new_node = Node([],[self])
        new_node.split_child_at(0)
        return new_node 
    
    def contains(self, num:int) -> bool: # NOTE: checking the number is within in the node 
        idx = self.search(num)
        return idx < self.num_keys() and self.keys[idx] == num 

    def delete(self, num:int) -> None: 
        if self.contains(num): 
            idx = self.search(num)
            del self.keys[idx]


    def predecessor(self, num:int) -> int | None: 
        #NOTE: case 2ab assumes that the left and the right have enough nodes 
        idx = self.search(num)

        if idx >= self.num_keys() or self.keys[idx] != num:
            return None 

        if idx < self.num_children(): 
            curr = self.children[idx]

            while not curr.is_leaf(): 
                curr = curr.children[-1]

            return curr.keys[-1] 

        return None 


    def successor(self, num:int)-> int | None: 
        # NOTE: case 2ab assumes that the left and the right have enough nodes  
        idx = self.search(num)

        if idx >= self.num_keys() or self.keys[idx] != num: 
            return None 

        if idx + 1 < self.num_children(): 
            curr = self.children[idx+1]
            while not curr.is_leaf():
                curr = curr.children[0]
            return curr.keys[0]

        return None 

    def merge(self, i): 

        median = self.keys[i]
        left, right = self.children[i:i+2]

        left.keys.append(median)
        left.keys.extend(right.keys)

        if not right.is_leaf():
            left.children.extend(right.children)

        del self.keys[i]
        del self.children[i+1]

        right.recalculate_count()
        left.recalculate_count()
        self.recalculate_count()
        

    def right_rotation(self, idx: int) -> None: 
        #NOTE: borrowing from the RHS 

        child = self.children[idx]
        rhs_sibling = self.children[idx+1]

        median = self.keys[idx]
        immediate_successor = rhs_sibling.keys[0]

        child.keys.append(median) # append the median to the RHS of child 

        self.keys[idx] = immediate_successor
        del rhs_sibling.keys[0] # removing the immediate_successor

        if not rhs_sibling.is_leaf(): 
            child.children.append(rhs_sibling.children[0])
            del rhs_sibling.children[0] # remove the children from the RHS 

        child.recalculate_count()
        rhs_sibling.recalculate_count()
        self.recalculate_count()

    def left_rotation(self, idx:int) -> None:

        child = self.children[idx]
        lhs_sibling = self.children[idx-1]

        median = self.keys[idx-1]
        immediate_predecessor = lhs_sibling.keys[-1]

        child.keys.insert(0, median)

        self.keys[idx-1] = immediate_predecessor 
        del lhs_sibling.keys[-1] # remove the predecessor

        if not lhs_sibling.is_leaf(): 
            child.children.insert(0, lhs_sibling.children[-1])
            del lhs_sibling.children[-1]

        child.recalculate_count()
        lhs_sibling.recalculate_count()
        self.recalculate_count()

class BTree:

    def __init__(self, t:int): 

        self.root = Node([],[])
        self.upper = 2*t - 1
        self.lower = t-1 

    def insert(self, num:int) -> None:    

        if self.root.num_keys() == self.upper: 
            self.root = self.root.split_new_root()

        self._insert_loop(num, self.root)

    def _insert_loop(self, num: int, curr: 'Node') -> None: 

        if curr.is_leaf():
            curr.insert_node(num)
            curr.recalculate_count()
            return 

        idx = curr.search(num)
        child = curr.children[idx]

        if child.num_keys() >= self.upper: 
            curr.split_child_at(idx)

            if curr.keys[idx] < num:
                idx += 1 

        self._insert_loop(num, curr.children[idx])
        curr.recalculate_count()

    def search(self, num:int) -> Tuple['Node', int] | Tuple[None, None]: 

        curr = self.root 
        idx = 0 

        while not curr.contains(num) and not curr.is_leaf(): 
            idx = curr.search(num)
            curr = curr.children[idx]

        return (curr, idx) if curr.contains(num) else (None, None)

    def delete(self, num:int) -> None:  

        node, idx = self.search(num)

        if not node: 
            return 

        curr = self.root 
        path = []

        while not curr.is_leaf(): 

            idx = curr.search(num)
            path.append(curr)

            # NOTE: here we find out if num in internal nodes
            if curr.contains(num): 

                left, right = curr.children[idx:idx+2]

                if left.num_keys() > self.lower:  
                    #NOTE: find predecessor 
                    pred = curr.predecessor(num) 
                    if pred: 
                        curr.keys[idx] = pred
                        num = pred

                elif right.num_keys() > self.lower: 
                    # NOTE: find successor
                    succ = curr.successor(num)
                    if succ: 
                        curr.keys[idx] = succ  
                        num = succ 
                        idx += 1 
                else: 
                    #NOTE: merge the LHS and the RHS 
                    curr.merge(idx)


            child = curr.children[idx]
            if child.num_keys() == self.lower: 

                sibling_lhs = curr.children[idx-1] if idx-1 >= 0 else None 
                sibling_rhs = curr.children[idx+1] if idx+1 < curr.num_children() else None

                # NOTE: 3b 
                if (sibling_lhs and sibling_lhs.num_keys() == self.lower): 
                    curr.merge(idx-1)
                    idx -= 1 
                elif (sibling_rhs and sibling_rhs.num_keys() == self.lower):
                    curr.merge(idx)

                #NOTE: 3a
                elif sibling_rhs and sibling_rhs.num_keys() > self.lower: 
                    curr.right_rotation(idx)
                elif sibling_lhs and sibling_lhs.num_keys() > self.lower: 
                    curr.left_rotation(idx)

            curr = curr.children[idx] 

        curr.delete(num)
        path.append(curr)

        for node in reversed(path): 
            node.recalculate_count()

        if self.root.num_keys() == 0 and not self.root.is_leaf(): 
            self.root = self.root.children[0]

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


def read_keys_from_file(filename: str) -> List[int]: 
    with open(filename, 'r') as file: 
        return [int(line.strip()) for line in file if line.strip()]

def process_commands(c: 'Commands', commands_file: str, output: str) -> None:
    with open(commands_file, 'r') as input_file, open(output, 'w') as output_file:
        for line in input_file:
            parts = line.strip().split()
            if not parts:
                continue

            command = parts[0]
            arguments = parts[1:]

            if command == "select":
                res = c.select(int(arguments[0]))
                output_file.write(f"{res}\n")

            elif command == "rank":
                res = c.rank(int(arguments[0]))
                output_file.write(f"{res}\n")

            elif command == "keysInRange":
                res = c.keysInRange(int(arguments[0]), int(arguments[1]))
                output_file.write("-1\n" if res == [-1] else " ".join(map(str, res)) + "\n")

            elif command == "primesInRange":
                res = c.primesInRange(int(arguments[0]), int(arguments[1]))
                output_file.write("-1\n" if res == [-1] else " ".join(map(str, res)) + "\n")

def main():
    t = int(sys.argv[1])
    keys_insert_file = sys.argv[2]
    keys_delete_file = sys.argv[3]
    commands_file = sys.argv[4]
    output_file = "output_a3.txt"

    c = Commands(t)
    c.insertKeys(read_keys_from_file(keys_insert_file))
    c.deleteKeys(read_keys_from_file(keys_delete_file))
    process_commands(c, commands_file, output_file)

if __name__ == '__main__':
    main()