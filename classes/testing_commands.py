from a3 import Commands as c
import unittest 
import random 

class rankSelect(unittest.TestCase): 

    def setUp(self): 

        random.seed(88)
        self.k_values = random.sample(range(2,10), 8)
        self.insertions = random.sample(range(0,100000000), 100000)
        self.selections = [i+1 for i in range(len(self.insertions)-2)]

    def test_rank_select(self): 
        for k in self.k_values: 
            commands = c(k)
            commands.insertKeys(self.insertions)
            
            positions_to_test = random.sample(range(1, commands.root.count + 1), min(10, commands.root.count))
            
            for s in positions_to_test:  
                res = commands.select(s)
                x = commands.rank(res)
                
                if x != s:
                    print(f"\nFAILURE at k={k}, s={s}")
                    print(f"select({s}) = {res}, rank({res}) = {x}")
                    
                self.assertEqual(x, s, f"Failed for select({s}) = {res}, rank({res}) = {x}")

class TestRangeFunctions(unittest.TestCase): 

    def setUp(self): 
        random.seed(88)
        self.k_values = [2, 5, 9]  # Test with different tree structures
        
        # Create a mix of numbers including known primes
        self.test_insertions = [
            # Small primes
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            # Small composites
            4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25,
            # Larger numbers
            100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
            # Some larger primes
            97, 113, 127, 131, 139, 149, 151, 157, 163, 167,
            # Edge cases
            1, 0, 
            # Larger range
            200, 250, 300, 350, 400, 450, 500,
            # Known larger primes
            211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
            269, 271, 277, 281, 283, 293, 307, 311, 313, 317
        ]
        
        # Shuffle to test with random insertion order
        random.shuffle(self.test_insertions)

    def test_keysInRange_basic(self):
        """Test basic functionality of keysInRange"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test 1: Range with multiple elements
            result = commands.keysInRange(10, 30)
            result_sorted = sorted(result)
            expected = [x for x in self.test_insertions if 10 <= x <= 30]
            expected_sorted = sorted(expected)
            
            self.assertEqual(result_sorted, expected_sorted, 
                           f"Failed for k={k}, range [10,30]. Got {result_sorted}, expected {expected_sorted}")

    def test_keysInRange_edge_cases(self):
        """Test edge cases for keysInRange"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test 1: Empty range (no elements in range)
            result = commands.keysInRange(1000, 2000)
            self.assertEqual(result, [-1], f"Failed empty range test for k={k}")
            
            # Test 2: Single element range
            result = commands.keysInRange(7, 7)
            self.assertEqual(result, [7], f"Failed single element test for k={k}")
            
            # Test 3: Range with lower > upper (invalid range)
            result = commands.keysInRange(100, 50)
            self.assertEqual(result, [-1], f"Failed invalid range test for k={k}")
            
            # Test 4: Range including min and max elements
            min_val = min(self.test_insertions)
            max_val = max(self.test_insertions)
            result = commands.keysInRange(min_val, max_val)
            result_sorted = sorted(result)
            expected_sorted = sorted(self.test_insertions)
            self.assertEqual(result_sorted, expected_sorted, 
                           f"Failed full range test for k={k}")

    def test_keysInRange_boundaries(self):
        """Test boundary conditions"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test 1: Range just before first element
            min_val = min(self.test_insertions)
            result = commands.keysInRange(min_val - 10, min_val - 1)
            self.assertEqual(result, [-1], f"Failed before-min test for k={k}")
            
            # Test 2: Range just after last element
            max_val = max(self.test_insertions)
            result = commands.keysInRange(max_val + 1, max_val + 10)
            self.assertEqual(result, [-1], f"Failed after-max test for k={k}")
            
            # Test 3: Range with some elements outside tree
            result = commands.keysInRange(-10, 10)
            result_sorted = sorted(result)
            expected = [x for x in self.test_insertions if -10 <= x <= 10]
            expected_sorted = sorted(expected)
            self.assertEqual(result_sorted, expected_sorted, 
                           f"Failed partial range test for k={k}")

    def test_primesInRange_basic(self):
        """Test basic functionality of primesInRange"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test 1: Range with known primes
            result = commands.primesInRange(1, 50)
            result_sorted = sorted(result)
            # Expected primes in range [1, 50] from our insertions
            expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            
            self.assertEqual(result_sorted, expected_primes, 
                           f"Failed prime test for k={k}, range [1,50]. Got {result_sorted}")

    def test_primesInRange_edge_cases(self):
        """Test edge cases for primesInRange"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test 1: Range with no primes
            result = commands.primesInRange(32, 36)  # No primes in this range in our data
            self.assertEqual(result, [-1], f"Failed no-primes test for k={k}")
            
            # Test 2: Range with only composite numbers
            composite_range = [x for x in self.test_insertions if 24 <= x <= 28]
            if composite_range:  # If we have numbers in this range
                result = commands.primesInRange(24, 28)
                # Should return -1 as there are no primes in 24-28
                self.assertEqual(result, [-1], f"Failed composite-only test for k={k}")
            
            # Test 3: Single prime
            result = commands.primesInRange(7, 7)
            self.assertEqual(result, [7], f"Failed single prime test for k={k}")
            
            # Test 4: Empty range
            result = commands.primesInRange(1000, 2000)
            self.assertEqual(result, [-1], f"Failed empty range prime test for k={k}")

    def test_primesInRange_composite_numbers(self):
        """Test that composite numbers are correctly excluded"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test range with mix of primes and composites
            result = commands.primesInRange(1, 20)
            
            # Verify no composite numbers in result
            composites_in_range = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
            for composite in composites_in_range:
                self.assertNotIn(composite, result, 
                               f"Composite {composite} incorrectly included for k={k}")

    def test_primesInRange_large_primes(self):
        """Test with larger prime numbers"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test larger range
            result = commands.primesInRange(200, 320)
            result_sorted = sorted(result)
            
            # Expected large primes from our insertions
            expected = [211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
                       269, 271, 277, 281, 283, 293, 307, 311, 313, 317]
            
            self.assertEqual(result_sorted, expected, 
                           f"Failed large primes test for k={k}")

    def test_range_after_deletions(self):
        """Test range functions after some deletions"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Delete some elements
            to_delete = [5, 10, 15, 20, 25]  # Mix of primes and composites
            commands.deleteKeys(to_delete)
            
            # Test keysInRange
            result = commands.keysInRange(1, 30)
            for deleted in to_delete:
                if 1 <= deleted <= 30:
                    self.assertNotIn(deleted, result, 
                                   f"Deleted key {deleted} still in range for k={k}")
            
            # Test primesInRange
            prime_result = commands.primesInRange(1, 30)
            self.assertNotIn(5, prime_result, f"Deleted prime 5 still in result for k={k}")
            
            # Verify other primes still there
            if prime_result != [-1]:
                self.assertIn(7, prime_result, f"Prime 7 missing for k={k}")
                self.assertIn(11, prime_result, f"Prime 11 missing for k={k}")

    def test_special_cases(self):
        """Test special cases like 1 and 0"""
        for k in self.k_values:
            commands = c(k)
            commands.insertKeys(self.test_insertions)
            
            # Test that 1 is not considered prime
            result = commands.primesInRange(1, 1)
            self.assertEqual(result, [-1], f"1 incorrectly identified as prime for k={k}")
            
            # Test that 0 is in keysInRange but not in primesInRange
            result_keys = commands.keysInRange(0, 5)
            result_primes = commands.primesInRange(0, 5)
            
            self.assertIn(0, result_keys, f"0 not in keysInRange for k={k}")
            if result_primes != [-1]:
                self.assertNotIn(0, result_primes, f"0 incorrectly in primesInRange for k={k}")

class TestInsertDelete(unittest.TestCase):
    def setUp(self):
        random.seed(88)
        self.k_values = [2, 5, 9]
        
    def test_insertions(self):
        """Test that insertions work correctly"""
        for k in self.k_values:
            commands = c(k)
            test_values = [50, 30, 70, 20, 60, 40, 80]
            
            commands.insertKeys(test_values)
            
            # Verify all values are in the tree
            for val in test_values:
                rank = commands.rank(val)
                self.assertNotEqual(rank, -1, f"Value {val} not found after insertion for k={k}")
                
            # Verify count is correct
            self.assertEqual(commands.root.count, len(test_values), 
                           f"Tree count incorrect after insertions for k={k}")
    
    def test_deletions(self):
        """Test that deletions work correctly"""
        for k in self.k_values:
            commands = c(k)
            test_values = list(range(1, 21))  # Insert 1-20
            
            commands.insertKeys(test_values)
            
            # Delete even numbers
            to_delete = [x for x in test_values if x % 2 == 0]
            commands.deleteKeys(to_delete)
            
            # Verify deleted values are gone
            for val in to_delete:
                rank = commands.rank(val)
                self.assertEqual(rank, -1, f"Value {val} still found after deletion for k={k}")
            
            # Verify remaining values are still there
            remaining = [x for x in test_values if x % 2 == 1]
            for val in remaining:
                rank = commands.rank(val)
                self.assertNotEqual(rank, -1, f"Value {val} missing after deletions for k={k}")
                
            # Verify count is correct
            self.assertEqual(commands.root.count, len(remaining), 
                           f"Tree count incorrect after deletions for k={k}")
if __name__ == '__main__': 
    unittest.main()


