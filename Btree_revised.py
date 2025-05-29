import random 
from node import Node 
from queue import Queue 
from collections import defaultdict 
from typing import Tuple, List, Dict

class BTree:

    def __init__(self, t:int): 

        self.root = Node([],[])
        self.upper = 2*t - 1
        self.lower = t-1 

    def insert_rec(self, num:int, curr: 'Node') -> None:    

        if self.root.num_keys() == self.upper: 
            self.root = self.root.split_new_root()

        if curr.is_leaf():
            curr.insert(num)
            curr.recalculate_count()
            return 

        idx = curr.search(num)
        child = curr.children[idx]

        if child.num_keys() >= self.upper: 
            curr.split_child_at(idx)

            if curr.keys[idx] < num:
                idx += 1 

        self.insert_rec(num, curr.children[idx])
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

    def breadth_first_search(self) -> Dict[int, List[int]]: 

        if not self.root: 
            return {} 

        layers = defaultdict(list)
        level = 0 
        queue = Queue() 
        queue.put([level, self.root])

        while not queue.empty(): 

            level, node = queue.get() 

            for child in node.children:
                queue.put([level+1, child])

            layers[level].append(node)

        return layers 

    
    def __str__(self): 
        layers = self.breadth_first_search()
        sorted_key_values = sorted(layers.items(), key=lambda x: x[0])
        output = ""
        for level, keys in sorted_key_values:
            output += f"Level {level}: {keys}\n"
        return output

if __name__ == '__main__': 
    random.seed(88)
    insertions =  random.sample(range(0,100), 10)

    c = BTree(3)

    for i in insertions: 
        c.insert_rec(i, c.root)

    print(c)


    
