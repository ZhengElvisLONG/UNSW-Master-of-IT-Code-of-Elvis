# Exercise 2: Analyze Runs
# Analyzes a list L of integers to find consecutive runs (sequences).
# A run is a maximal consecutive sublist that is either strictly increasing or strictly decreasing.
# Only runs of length at least 2 are considered.
# Output the runs found, grouped by type ('Increasing' or 'Decreasing'),
# sorted by their starting index within the original list.
# For each run, print its type, starting index, and length.
#
# You can assume that the argument L to analyze_runs() is a list of integers.
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def analyze_runs(L):
    """
    Identifies and reports strictly increasing or decreasing runs of length >= 2.
    
    >>> analyze_runs([])
    No runs found.
    >>> analyze_runs([1, 2])
    Increasing runs:
      Start index 0, length 2
    Decreasing runs:
      None
    >>> analyze_runs([2, 1])
    Increasing runs:
      None
    Decreasing runs:
      Start index 0, length 2
    >>> analyze_runs([1, 1, 1])
    No runs found.
    >>> analyze_runs([5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1])
    Increasing runs:
      Start index 4, length 5
    Decreasing runs:
      Start index 0, length 5
      Start index 8, length 5
    >>> analyze_runs([10, 20, 15, 25, 30, 5, 0])
    Increasing runs:
      Start index 0, length 2
      Start index 2, length 3
    Decreasing runs:
      Start index 1, length 2
      Start index 4, length 3
    """
    # if not L or len(L) < 2:
    #     print("No runs found.")
    #     return

    # increasing_runs = []
    # decreasing_runs = []
    # i = 0
    # while i < len(L) - 1:
    #     start_index = i
    #     # Check for increasing run
    #     if L[i+1] > L[i]:
    #         while i < len(L) - 1 and L[i+1] > L[i]:
    #             i += 1
    #         if i - start_index >= 1: # Length >= 2
    #             increasing_runs.append((start_index, i - start_index + 1))
    #     # Check for decreasing run
    #     elif L[i+1] < L[i]:
    #         while i < len(L) - 1 and L[i+1] < L[i]:
    #             i += 1
    #         if i - start_index >= 1: # Length >= 2
    #             decreasing_runs.append((start_index, i - start_index + 1))
    #     else: # L[i+1] == L[i]
    #         i += 1
            
    # if not increasing_runs and not decreasing_runs:
    #     print("No runs found.")
    #     return

    # print("Increasing runs:")
    # if increasing_runs:
    #     for start, length in increasing_runs:
    #         print(f"  Start index {start}, length {length}")
    # else:
    #     print("  None")

    # print("Decreasing runs:")
    # if decreasing_runs:
    #     for start, length in decreasing_runs:
    #         print(f"  Start index {start}, length {length}")
    # else:
    #     print("  None")
    increase, decrease = [], []
    increase_start, decrease_start, increase_time, decrease_time = 0, 0, 0, 0
    for i in range(len(L) - 1):
        if L[i] < L[i + 1]:
            increase_time += 1
            if decrease_time:
              decrease.append((decrease_start, decrease_time + 1))
              decrease_time = 0
              increase_start = i
        if L[i] > L[i + 1]:
            decrease_time += 1
            if increase_time:
              increase.append((increase_start, increase_time + 1))
              increase_time = 0
              decrease_start = i
        if L[i] == L[i + 1]:
           if (decrease_start, decrease_time + 1) not in decrease and decrease_time not in [0]:
              decrease.append((decrease_start, decrease_time + 1))
           if (increase_start, increase_time + 1) not in increase and increase_time not in [0]:
              increase.append((increase_start, increase_time + 1))
           increase_time, decrease_time = 0, 0
    if (decrease_start, decrease_time + 1) not in decrease and decrease_time not in [0]:
       decrease.append((decrease_start, decrease_time + 1))
    if (increase_start, increase_time + 1) not in increase and increase_time not in [0]:
       increase.append((increase_start, increase_time + 1))
    if not increase and not decrease or len(L) < 2:
       print("No runs found.")
       return
    print("Increasing runs:")
    if increase:
       for pair in increase:
          print(f"  Start index {pair[0]}, length {pair[1]}")
    else:
       print("  None")
    print("Decreasing runs:")
    if decrease:
       for pair in decrease:
          print(f"  Start index {pair[0]}, length {pair[1]}")
    else:
       print("  None")
if __name__ == '__main__':
    import doctest
    doctest.testmod()

