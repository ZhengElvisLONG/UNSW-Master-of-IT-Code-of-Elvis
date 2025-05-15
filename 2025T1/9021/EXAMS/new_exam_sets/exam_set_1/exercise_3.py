# Exercise 3: Solve Multiplication Equation
# You can assume that the argument to solve() is of the form
# x*y=z where:
# - x, y and z are NONEMPTY sequences of UNDERSCORES and DIGITS;
# - there can be any number of spaces (possibly none) before x,
#   between x and *, between * and y, between y and =, between = and z,
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
# * and =, with no leading nor trailing spaces, and without extra leading 0s
# in front of an integer.

def solve_multiplication(equation):
    """
    Solves equations of the form x * y = z with underscores.
    
    >>> solve_multiplication("1 * 2 = 3")
    No solution!
    >>> solve_multiplication("12 * _ = 36")
    12 * 3 = 36
    >>> solve_multiplication("__ * 1 = 11")
    11 * 1 = 11
    >>> solve_multiplication(" _ * _ = 4 ")
    2 * 2 = 4
    >>> solve_multiplication(" 21 * _ = 12_ ")
    21 * 6 = 126
    >>> solve_multiplication(" _3 * _3 = 169 ")
    13 * 13 = 169
    >>> solve_multiplication(" 1_ * _1 = 271 ")
    No solution!
    >>> solve_multiplication(" _ * 1_ = 1_ ") # Multiple solutions
    1 * 11 = 11
    >>> solve_multiplication(" 0 * _ = _ ") # Multiple solutions
    0 * 0 = 0
    >>> solve_multiplication(" _ * _ = _ ") # Multiple solutions
    0 * 0 = 0
    1 * 1 = 1
    """
    # equation = equation.replace(" ", "")
    # parts = equation.split("*")
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
    #                if not (x_str == "0" or y_str == "0" or z_str == "0"): # Allow single "0"
    #                    continue
                       
    #             x_num = int(x_str)
    #             y_num = int(y_str)
    #             z_num = int(z_str)
                
    #             if x_num * y_num == z_num:
    #                 # Check if the calculated z_num matches the pattern in z_str
    #                 # This handles cases like _ * _ = _ where 2*5=10 doesn't fit _
    #                 if str(z_num) == z_str.lstrip("0") or (z_num == 0 and z_str.count("0") == len(z_str)):
    #                      solutions.append((d_int, f"{x_num} * {y_num} = {z_num}"))
    #                 # Need a more robust check for pattern matching
    #                 temp_z_str = z_part.replace("_", d)
    #                 if str(z_num) == temp_z_str or (z_num == 0 and all(c == '0' for c in temp_z_str)):
    #                      # Check if the number of digits matches if z_part had underscores
    #                      if "_" in z_part:
    #                          if len(str(z_num)) == len(temp_z_str) or (z_num == 0 and len(temp_z_str) == 1):
    #                              solutions.append((d_int, f"{x_num} * {y_num} = {z_num}"))
    #                      else:
    #                          # If z_part had no underscores, just check equality
    #                          if z_num == int(z_part):
    #                              solutions.append((d_int, f"{x_num} * {y_num} = {z_num}"))

    #         except ValueError:
    #             continue # Skip if conversion fails (e.g., empty string after replace?)
    # else:
    #     try:
    #         x_num = int(x_part)
    #         y_num = int(y_part)
    #         z_num = int(z_part)
    #         if x_num * y_num == z_num:
    #             solutions.append((0, f"{x_num} * {y_num} = {z_num}"))
    #     except ValueError:
    #         pass

    # # Remove duplicates and sort
    # unique_solutions = sorted(list(set(solutions)), key=lambda x: (x[0], x[1]))

    # if not unique_solutions:
    #     print("No solution!")
    # else:
    #     # Refine the check for _ * _ = _ case
    #     if x_part == "_" and y_part == "_" and z_part == "_":
    #         final_solutions = []
    #         seen_digits = set()
    #         for d_int, sol_str in unique_solutions:
    #              parts = sol_str.split(" = ")
    #              if len(parts[1]) == 1 and d_int not in seen_digits:
    #                  final_solutions.append(sol_str)
    #                  seen_digits.add(d_int)
    #         final_solutions.sort(key=lambda s: int(s.split(" * ")[0])) # Sort by first number primarily
    #         for sol in final_solutions:
    #              print(sol)
    #     else:
    #         for _, sol in unique_solutions:
    #             print(sol)
    equation = equation.replace(" ", "")
    temp = equation.split("*")
    a = temp[0]
    temp = temp[1].split("=")
    b, c = temp[0], temp[1]
    mul = [a, b, c]
    for i in range(len(mul)):
        if mul[i] != '0':
            mul[i] = mul[i].lstrip('0') 
    a, b, c = mul[0], mul[1], mul[2]
    if "_" not in a + b + c:
        if int(a) * int(b) == int(c):
            print(f"{a} * {b} = {c}")
        else:
            print("No solution!")
        return
    mul_new = [0, 0, 0]
    has_solution = False
    for i in range(10):
        for j in range(3):
            mul_new[j] = int(mul[j].replace("_", str(i)))
        if mul_new[0] * mul_new[1] == mul_new[2]:
            print(f"{mul_new[0]} * {mul_new[1]} = {mul_new[2]}")
            has_solution = True
    if not has_solution:
        print("No solution!")


if __name__ == '__main__':
    import doctest
    # Need to refine the logic for _ * _ = _ case in the doctest itself or the function
    # The current doctest for _ * _ = _ might be too broad or the logic needs adjustment
    # Let's adjust the function logic slightly for the _ * _ = _ case
    # Re-running doctest after potential adjustments
    doctest.testmod()

