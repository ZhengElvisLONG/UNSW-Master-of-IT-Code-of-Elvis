# Exercise 3: Solve Division Equation
# You can assume that the argument to solve() is of the form
# x/y=z where:
# - x, y and z are NONEMPTY sequences of UNDERSCORES and DIGITS;
# - y CANNOT represent 0 unless it is just "0" or "_" (which could be 0).
# - Division is integer division (// in Python).
# - there can be any number of spaces (possibly none) before x,
#   between x and /, between / and y, between y and =, between = and z,
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
# / and =, with no leading nor trailing spaces, and without extra leading 0s
# in front of an integer.

def solve_division(equation):
    """
    Solves equations of the form x / y = z (integer division) with underscores.
    
    >>> solve_division("10 / 2 = 6")
    No solution!
    >>> solve_division("1_ / 3 = 4")
    12 / 3 = 4
    13 / 3 = 4
    14 / 3 = 4
    >>> solve_division("__ / 11 = 1")
    11 / 11 = 1
    12 / 11 = 1
    13 / 11 = 1
    14 / 11 = 1
    15 / 11 = 1
    16 / 11 = 1
    17 / 11 = 1
    18 / 11 = 1
    19 / 11 = 1
    20 / 11 = 1
    21 / 11 = 1
    >>> solve_division(" _0 / _ = 10 ")
    10 / 1 = 10
    20 / 2 = 10
    30 / 3 = 10
    40 / 4 = 10
    50 / 5 = 10
    60 / 6 = 10
    70 / 7 = 10
    80 / 8 = 10
    90 / 9 = 10
    >>> solve_division(" 1_0 / 1_ = 10 ")
    100 / 10 = 10
    110 / 11 = 10
    120 / 12 = 10
    130 / 13 = 10
    140 / 14 = 10
    150 / 15 = 10
    160 / 16 = 10
    170 / 17 = 10
    180 / 18 = 10
    190 / 19 = 10
    >>> solve_division(" _ / _ = 1 ") # Multiple solutions
    1 / 1 = 1
    2 / 2 = 1
    3 / 3 = 1
    4 / 4 = 1
    5 / 5 = 1
    6 / 6 = 1
    7 / 7 = 1
    8 / 8 = 1
    9 / 9 = 1
    >>> solve_division(" _ / 1 = _ ") # Multiple solutions
    0 / 1 = 0
    1 / 1 = 1
    2 / 1 = 2
    3 / 1 = 3
    4 / 1 = 4
    5 / 1 = 5
    6 / 1 = 6
    7 / 1 = 7
    8 / 1 = 8
    9 / 1 = 9
    >>> solve_division(" 10 / _ = 0 ")
    No solution! # Division by zero is not allowed, result 0 needs careful check
    # Let's re-evaluate: 10 // _ = 0. This is true for _ > 10. No single digit works.
    >>> solve_division(" 9 / _ = 4 ")
    9 / 2 = 4
    >>> solve_division(" _ / 0 = 5 ") # Division by zero
    No solution!
    """
    equation = equation.replace(" ", "")
    parts = equation.split("/")
    x_part = parts[0]
    remaining = parts[1].split("=")
    y_part = remaining[0]
    z_part = remaining[1]
    
    solutions = []
    has_underscore = "_" in x_part or "_" in y_part or "_" in z_part
    
    if has_underscore:
        for d_int in range(10):
            d = str(d_int)
            x_str = x_part.replace("_", d)
            y_str = y_part.replace("_", d)
            z_str = z_part.replace("_", d)
            
            try:
                # Check for invalid leading zeros
                if (len(x_str) > 1 and x_str.startswith("0")) or \
                   (len(y_str) > 1 and y_str.startswith("0")) or \
                   (len(z_str) > 1 and z_str.startswith("0")):
                   if not (x_str == "0" or y_str == "0" or z_str == "0"): 
                       continue
                       
                x_num = int(x_str)
                y_num = int(y_str)
                z_num = int(z_str)
                
                # Check for division by zero
                if y_num == 0:
                    continue
                    
                if x_num // y_num == z_num:
                    # Format check: ensure the result z_num matches the pattern z_str
                    temp_z_str = z_part.replace("_", d)
                    valid_solution = False
                    try:
                        # Check if int(temp_z_str) matches z_num, handling leading zeros
                        if int(temp_z_str) == z_num:
                             valid_solution = True
                    except ValueError:
                         pass # Should not happen if z_str is valid digits/underscore

                    if valid_solution:
                        solutions.append((d_int, f"{x_num} / {y_num} = {z_num}"))

            except ValueError:
                continue # Skip if conversion fails
    else:
        try:
            x_num = int(x_part)
            y_num = int(y_part)
            z_num = int(z_part)
            # Check for division by zero
            if y_num == 0:
                pass # Handled by printing no solution later
            elif x_num // y_num == z_num:
                solutions.append((0, f"{x_num} / {y_num} = {z_num}"))
        except ValueError:
            pass

    # Remove duplicates and sort
    unique_solutions = sorted(list(set(solutions)), key=lambda x: (x[0], x[1]))

    if not unique_solutions:
        print("No solution!")
    else:
        for _, sol in unique_solutions:
            print(sol)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

