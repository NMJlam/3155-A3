from typing import List

class Node: 

    def __init__(self, keys: List[int], children: List['Node']) -> None: 
        self.keys = keys 
        self.children = children 
        self.count = 0

        if children: 
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

    def __repr__(self): 
        return f"({self.count} | {self.keys})"
    def __str__(self): 
        return f"({self.count} | {self.keys})"

if __name__ == '__main__': 
    left = Node([123],[])
    right = Node([456],[])
    
    root = Node([0], [left,right])
    root.split_child_at(0)

