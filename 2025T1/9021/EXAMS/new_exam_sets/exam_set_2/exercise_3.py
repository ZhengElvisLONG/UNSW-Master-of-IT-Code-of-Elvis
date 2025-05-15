# Exercise 3: Solve Subtraction Equation
# You can assume that the argument to solve() is of the form
# x-y=z where:
# - x, y and z are NONEMPTY sequences of UNDERSCORES and DIGITS;
# - there can be any number of spaces (possibly none) before x,
#   between x and -, between - and y, between y and =, between = and z,
#   and after z.
#
# ALL OCCURRENCES OF _ ARE MEANT TO BE REPLACED BY THE SAME DIGIT.
#
# Note that sequences of digits such as 000 and 00037 represent
# 0 and 37, consistently with what int("000") and int("00037") return,
# respectively.
#
# When there is more than one solution, solutions are output from
# smallest to largest values of _.
#
# Note that an equation is always output with a single space before and after
# - and =, with no leading nor trailing spaces, and without extra leading 0s
# in front of an integer.

def solve_subtraction(equation):
    """
    Solves equations of the form x - y = z with underscores.
    
    >>> solve_subtraction("10 - 2 = 7")
    No solution!
    >>> solve_subtraction("1_ - 5 = 8")
    13 - 5 = 8
    >>> solve_subtraction("__ - 1 = 10")
    11 - 1 = 10
    >>> solve_subtraction(" _5 - _ = 50 ")
    55 - 5 = 50
    >>> solve_subtraction(" 1_3 - 1_ = 111 ")
    123 - 12 = 111
    >>> solve_subtraction(" _00 - 1__ = 1 ")
    200 - 199 = 1
    >>> solve_subtraction(" 10 - _ = _ ") # Multiple solutions
    10 - 1 = 9
    10 - 2 = 8
    10 - 3 = 7
    10 - 4 = 6
    10 - 5 = 5
    >>> solve_subtraction(" _ - _ = 0 ") # Multiple solutions
    0 - 0 = 0
    1 - 1 = 0
    2 - 2 = 0
    3 - 3 = 0
    4 - 4 = 0
    5 - 5 = 0
    6 - 6 = 0
    7 - 7 = 0
    8 - 8 = 0
    9 - 9 = 0
    >>> solve_subtraction(" 1_ - _1 = 0 ")
    No solution!
    >>> solve_subtraction(" _ - 0 = _ ") # Multiple solutions
    0 - 0 = 0
    1 - 0 = 1
    2 - 0 = 2
    3 - 0 = 3
    4 - 0 = 4
    5 - 0 = 5
    6 - 0 = 6
    7 - 0 = 7
    8 - 0 = 8
    9 - 0 = 9
    """
    # equation = equation.replace(" ", "")
    # parts = equation.split("-")
    # x_part = parts[0]
    # remaining = parts[1].split("=")
    # y_part = remaining[0]
    # z_part = remaining[1]
    
    # solutions = []
    # has_underscore = "_" in x_part or "_" in y_part or "_" in z_part
    
    # if has_underscore:
    #     for d_int in range(10):
    #         d = str(d_int)
    #         x_str = x_part.replace("_", d)
    #         y_str = y_part.replace("_", d)
    #         z_str = z_part.replace("_", d)
            
    #         try:
    #             # Check for invalid leading zeros (e.g., "_1" becoming "01" if d=0)
    #             if (len(x_str) > 1 and x_str.startswith("0")) or \
    #                (len(y_str) > 1 and y_str.startswith("0")) or \
    #                (len(z_str) > 1 and z_str.startswith("0")):
    #                # Allow single "0" or cases like "0" - "0" = "0"
    #                is_zero_case = (x_str == "0" and y_str == "0" and z_str == "0")
    #                if not is_zero_case and not (x_str == "0" or y_str == "0" or z_str == "0"):
    #                    if not (len(x_str) == 1 and x_str == "0") and \
    #                       not (len(y_str) == 1 and y_str == "0") and \
    #                       not (len(z_str) == 1 and z_str == "0"):
    #                        continue
                       
    #             x_num = int(x_str)
    #             y_num = int(y_str)
    #             z_num = int(z_str)
                
    #             if x_num - y_num == z_num:
    #                 # Format check: ensure the result z_num matches the pattern z_str
    #                 temp_z_str = z_part.replace("_", d)
    #                 # Handle negative zero case implicitly by int conversion
    #                 formatted_z = str(z_num)
                    
    #                 # Check if formatted_z matches temp_z_str pattern
    #                 matches = False
    #                 if len(formatted_z) == len(temp_z_str):
    #                     matches = True
    #                     for i in range(len(formatted_z)):
    #                         if temp_z_str[i] != "_" and temp_z_str[i] != formatted_z[i]:
    #                             matches = False
    #                             break
    #                 elif z_num == 0 and all(c == '0' for c in temp_z_str): # Special case for all zeros
    #                      matches = True
    #                 elif len(temp_z_str) > 1 and temp_z_str.startswith("0") and formatted_z == temp_z_str.lstrip("0"):
    #                      # Case like _0 - _ = 0 where _=1 -> 10 - 10 = 0, z_str is 0
    #                      matches = True
                         
    #                 # Simplified check: if z_part had underscores, does str(z_num) fit the pattern?
    #                 # If z_part had no underscores, does z_num equal int(z_part)?
    #                 valid_solution = False
    #                 if "_" in z_part:
    #                     # Check if str(z_num) could be formed by replacing _ in z_part with d
    #                     # This is tricky. Let's rely on the direct comparison for now.
    #                     # A more robust check might involve regex or careful string comparison.
    #                     # Let's try comparing int(temp_z_str) if possible
    #                     try:
    #                         if int(temp_z_str) == z_num:
    #                             valid_solution = True
    #                     except ValueError: # temp_z_str might be like "01" when z_num is 1
    #                          if z_num == int(temp_z_str.lstrip("0") if len(temp_z_str)>1 else temp_z_str):
    #                              valid_solution = True
    #                 else:
    #                     if z_num == int(z_part):
    #                         valid_solution = True
                            
    #                 if valid_solution:
    #                     solutions.append((d_int, f"{x_num} - {y_num} = {z_num}"))

    #         except ValueError:
    #             continue # Skip if conversion fails
    # else:
    #     try:
    #         x_num = int(x_part)
    #         y_num = int(y_part)
    #         z_num = int(z_part)
    #         if x_num - y_num == z_num:
    #             solutions.append((0, f"{x_num} - {y_num} = {z_num}"))
    #     except ValueError:
    #         pass

    # # Remove duplicates and sort
    # unique_solutions = sorted(list(set(solutions)), key=lambda x: (x[0], x[1]))

    # if not unique_solutions:
    #     print("No solution!")
    # else:
    #     for _, sol in unique_solutions:
    #         print(sol)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

