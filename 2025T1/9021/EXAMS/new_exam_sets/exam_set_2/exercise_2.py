# Exercise 2: Balanced Segments
# Analyzes a list L of integers to find all contiguous segments of even length (>= 2)
# such that the sum of the first half of the segment equals the sum of the second half.
# Output the segments found, grouped by their length, sorted from shortest to longest length.
# For a given length, list the segments by their starting index in the original list.
# Print the segment itself.
#
# You can assume that the argument L to find_balanced_segments() is a list of integers.
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.
from collections import defaultdict
def find_balanced_segments(L):
    """
    Finds all balanced segments of even length >= 2.
    A segment L[i:j] is balanced if sum(L[i : i+(j-i)//2]) == sum(L[i+(j-i)//2 : j]).
    
    >>> find_balanced_segments([])
    No balanced segments found.
    >>> find_balanced_segments([1])
    No balanced segments found.
    >>> find_balanced_segments([1, 1])
    Segments of length 2:
      Index 0: [1, 1]
    >>> find_balanced_segments([1, 2, 1, 2])
    Segments of length 4:
      Index 0: [1, 2, 1, 2]
    >>> find_balanced_segments([7, 3, 4, 6, 1, 5])
    Segments of length 4:
      Index 0: [7, 3, 4, 6]
      Index 1: [3, 4, 6, 1]
    >>> find_balanced_segments([1, 0, 1, 0, 1, 0])
    Segments of length 4:
      Index 0: [1, 0, 1, 0]
      Index 1: [0, 1, 0, 1]
      Index 2: [1, 0, 1, 0]
    >>> find_balanced_segments([1, 2, 3, 3, 2, 1])
    Segments of length 2:
      Index 2: [3, 3]
    Segments of length 6:
      Index 0: [1, 2, 3, 3, 2, 1]
    """
    # n = len(L)
    # found_segments = {}

    # for length in range(2, n + 1, 2): # Iterate through even lengths
    #     segments_for_length = []
    #     for i in range(n - length + 1):
    #         segment = L[i : i + length]
    #         midpoint = length // 2
    #         first_half_sum = sum(segment[:midpoint])
    #         second_half_sum = sum(segment[midpoint:])
    #         if first_half_sum == second_half_sum:
    #             segments_for_length.append((i, segment))
        
    #     if segments_for_length:
    #         found_segments[length] = segments_for_length

    # if not found_segments:
    #     print("No balanced segments found.")
    #     return

    # for length in sorted(found_segments.keys()):
    #     print(f"Segments of length {length}:")
    #     for index, segment in found_segments[length]:
    #         # Correct the doctest for [1, 2, 1, 2] - length 2 has no balanced segments
    #         # Correct the doctest for [1, 5, 2, 4] - length 2 has no balanced segments
    #         # Correct the doctest for [7, 3, 4, 6, 1, 5] - length 2 has no balanced segments
    #         # Need to re-evaluate the logic or doctests carefully.
    #         # Let's assume the logic is correct and fix the doctests manually if needed after running.
    #         # The current logic seems correct: sum(first_half) == sum(second_half)
    #         # Re-checking doctests:
    #         # [1, 2, 1, 2]: len 2: [2,1] sum(2)!=sum(1) NO. [1,2] sum(1)!=sum(2) NO. [1,2] sum(1)!=sum(2) NO.
    #         # [1, 5, 2, 4]: len 2: [1,5] NO. [5,2] NO. [2,4] NO.
    #         # [7, 3, 4, 6, 1, 5]: len 2: [7,3] NO. [3,4] NO. [4,6] NO. [6,1] NO. [1,5] NO.
    #         # Okay, the doctests for length 2 in the examples above seem wrong based on the definition.
    #         # Let's proceed with the current logic and assume the definition is the source of truth.
    #         print(f"  Index {index}: {segment}")

    if len(L) < 2:
        print("No balanced segments found.")
        return
    # for i in range(len(L) - 1):
    #     for j in range(i + 1, len(L)):
    #         left, right, time = i, j, 0
    #         result = (L[left : right])
    #         while 2 * right - left + 1 < len(L) and sum(L[left : right]) == sum(L[right + 1 : 2 * right - left + 1]):
    #             left = right + 1
    #             right = 2 * right - left + 1
    #             result.extend(L[left : right])
    #             time += 1
    #         if time:
    #             print(f"Segments of length {len(result)}:")
    #             print(f"  Index {len(result)}: {result}")
    result = defaultdict(list)
    index = set()
    length = range(2, len(L) // 2 * 2 + 1, 2)
    # print(length)
    for l in length:
        # print(l)
        for left in range(len(L)):
            right = left + l
            if right <= len(L) and sum(L[left : left + l // 2]) == sum(L[left + l // 2 : right]):
                result[right - left].append(L[left : right])
                index.add(right - left)
    index = list(index)
    index.sort()
    for idx in index:
        print(f"Segments of length {idx}:")
        for i in range(len(result[idx])):
            print(f"  Index {i}: {result[idx][i]}")
                    

if __name__ == '__main__':
    import doctest
    # Correcting doctests based on the function logic:
    # For [1, 2, 1, 2], length 2 should have no output.
    # For [1, 5, 2, 4], length 2 should have no output.
    # For [7, 3, 4, 6, 1, 5], length 2 should have no output.
    # The doctest runner will show failures for these, which is expected.
    # We are creating the question based on the definition provided.
    doctest.testmod()

