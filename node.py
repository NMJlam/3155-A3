from typing import * 

class Node: 

    def __init__(self, keys: List[int], children: List['Node']) -> None: 
        self.keys = keys 
        self.children = children 

    def num_keys(self) -> int: 
        return len(self.keys)

    def num_children(self) -> int: 
        return len(self.children)

    def is_leaf(self) -> bool: 
        return self.num_children() == 0 

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
    
    def insert(self, num:int) -> None: 
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

    def split_new_root(self) -> None: 
        new_node = Node([],[self])
        new_node.split_child_at(0)
        return new_node 
    
    def contains(self, num:int) -> int: # NOTE: checking the number is within in the node 
        idx = self.search(num)
        return idx < self.num_keys() and self.keys[idx] == num 

    def delete(self, num:int) -> None: 
        if self.contains(num): 
            idx = self.search(num)
            del self.keys[idx]


    def predecessor(self, num:int) -> int: 
        #NOTE: case 2ab assumes that the left and the right have enough nodes 
        idx = self.search(num)

        if idx >= self.num_keys() or self.keys[idx] != num:
            return None 

        if idx < self.num_children(): 
            curr = self.children[idx]

            while not curr.is_leaf(): 
                curr = curr.children[-1]

            predecessor = curr.keys[-1]
            del curr.keys[-1]
            return predecessor 

        return None 


    def successor(self, num:int) -> int: 
        # NOTE: case 2ab assumes that the left and the right have enough nodes  
        idx = self.search(num)

        if idx >= self.num_keys() or self.keys[idx] != num: 
            return None 

        if idx + 1 < self.num_children(): 
            curr = self.children[idx+1]
            while not curr.is_leaf():
                curr = curr.children[0]

            successor = curr.keys[0]
            del curr.keys[0]
            return successor 

        return None 

    def merge(self, i): 

        left, right = self.children[i:i+2]

        left.keys.extend(right.keys)

        if not right.is_leaf():
            left.children.extend(right.children)

        del self.keys[i]
        del self.children[i]

    def __repr__(self): 
        return f"{self.keys}"
    def __str__(self): 
        return f"{self.keys}"

if __name__ == '__main__': 
    left = Node([123],[])
    right = Node([456],[])
    
    root = Node([0], [left,right])
    root.split_child_at(0)

