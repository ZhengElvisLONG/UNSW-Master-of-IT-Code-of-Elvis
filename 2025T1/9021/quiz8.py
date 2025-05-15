# Written by Zheng LONG for COMP9021
# Enhanced with detailed comments and improved variable names
#
# Creates a class to represent a permutation of 1, 2, ..., n for some n >= 0.
#
# An object is created by passing as argument to the class name:
# - either no argument, in which case the empty permutation is created, or
# - "length = n" for some n >= 0, in which case the identity over 1, ..., n
#   is created, or
# - the numbers 1, 2, ..., n for some n >= 0, in some order, possibly together
#   with "length = n".
#
# __len__(), __repr__() and __str__() are implemented, the latter providing
# the standard form decomposition of the permutation into cycles
# (see wikipedia page on permutations for details).
# - A given cycle starts with the largest value in the cycle.
# - Cycles are given from smallest first value to largest first value.
#
# Objects have:
# - nb_of_cycles as an attribute
# - inverse() as a method
#
# The * operator is implemented for permutation composition, for both infix
# and in-place uses, thanks to the __mul__() and __imul__() special methods,
# respectively.


class PermutationError(Exception):
    pass


class Permutation:
    def __init__(self, *args, length=None):
        # Handle empty permutation (no arguments provided)
        if not args and length is None:
            self.permutation_elements, self.nb_of_cycles = [], 0
            return
        
        # Handle identity permutation case (only length given)
        if not args and isinstance(length, int) and length >= 0:
            self.permutation_elements = [i for i in range(1, length + 1)]
            self.nb_of_cycles = length  # Identity maps each element to itself
            return
        
        # Validate input types and values
        error_msg = 'Cannot generate permutation from these arguments'
        if any(not isinstance(x, int) or x < 1 for x in args):
            raise PermutationError(error_msg)
        if length is not None and (not isinstance(length, int) or length < 0):
            raise PermutationError(error_msg)
        
        # Process permutation elements
        perm_data = list(args)
        distinct_vals = set(perm_data)
        
        # Check for duplicates and validate completeness
        if len(distinct_vals) != len(perm_data):
            raise PermutationError(error_msg)
        
        highest_val = max(perm_data) if perm_data else 0
        if length is not None and length != highest_val:
            raise PermutationError(error_msg)
        
        # Verify all numbers from 1 to max are included
        if distinct_vals != {n for n in range(1, highest_val + 1)}:
            raise PermutationError(error_msg)
        
        # Store permutation and calculate cycle structure
        self.permutation_elements = perm_data
        self._calculate_cycles()

    def _calculate_cycles(self):
        # Handle empty permutation case
        if not self.permutation_elements:
            self.nb_of_cycles = 0
            return
        
        tracked = set()
        cycles = []
        
        # Create direct lookup for permutation mapping
        perm_map = dict(zip(range(1, len(self.permutation_elements) + 1), 
                            [self.permutation_elements[i-1] for i in range(1, len(self.permutation_elements) + 1)]))
        
        # Detect all cycle structures
        for seed in range(1, len(self.permutation_elements) + 1):
            if seed in tracked: continue
            orbit = []
            cursor = seed
            
            # Traverse through cycle until complete
            while cursor not in tracked:
                tracked.add(cursor)
                orbit.append(cursor)
                cursor = perm_map[cursor]
            
            cycles.append(orbit)
        
        self.nb_of_cycles = len(cycles)

    def __len__(self):
        return len(self.permutation_elements)

    def __repr__(self):
        return 'Permutation()' if not self.permutation_elements else \
            f"Permutation({', '.join(str(x) for x in self.permutation_elements)})"

    def __str__(self):
        # Handle empty case
        if not self.permutation_elements: return '()'
        
        marked = set()
        orbits = []
        
        # Create element mapping dictionary
        img = {i: val for i, val in enumerate(self.permutation_elements, 1)}
        
        # Extract all disjoint cycles
        for start in range(1, len(self.permutation_elements) + 1):
            if start in marked: continue
            
            cycle = []
            pos = start
            
            # Extract single complete cycle
            while pos not in marked:
                marked.add(pos)
                cycle.append(pos)
                pos = img[pos]
            
            # Canonicalize cycle - rotate to start with maximum element
            if cycle:
                largest = max(cycle)
                pivot = cycle.index(largest)
                cycle = cycle[pivot:] + cycle[:pivot]
                orbits.append(cycle)
        
        # Sort cycles by first element (which is the largest in each cycle)
        orbits.sort(key=lambda c: c[0])
        
        # Format cycles into standard notation
        result = ''
        for c in orbits:
            result += f"({c[0]})" if len(c) == 1 else f"({' '.join(map(str, c))})"
        
        return result

    def __mul__(self, other_permutation):
        # Verify compatible dimensions
        if len(self) != len(other_permutation):
            raise PermutationError('Cannot compose permutations of different lengths')
        
        # Calculate functional composition (self followed by other)
        result = [other_permutation.permutation_elements[self.permutation_elements[i-1] - 1] 
                for i in range(1, len(self) + 1)]
        
        return Permutation(*result)

    def __imul__(self, other_permutation):
        # Check dimension compatibility
        if len(self) != len(other_permutation):
            raise PermutationError('Cannot compose permutations of different lengths')
        
        # Apply composition directly
        self.permutation_elements = [other_permutation.permutation_elements[self.permutation_elements[i-1] - 1] 
                                    for i in range(1, len(self) + 1)]
        
        # Update cycle structure after modification
        self._calculate_cycles()
        return self

    def inverse(self):
        # Create array to hold inverse mapping
        inv = [0] * len(self)
        
        # For each image value, record its preimage position
        for idx, target in enumerate(self.permutation_elements, 1):
            inv[target - 1] = idx
        
        return Permutation(*inv)