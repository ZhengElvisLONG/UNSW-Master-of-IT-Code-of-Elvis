# Written by *** for COMP9021
#
# Two functions to implement.
#
#
# The function frieze() takes an integer as argument,
# that you can assume is at least equal to 1;
# it prints out a "frieze", that note has no trailing
# spaces on any line.
#
#
# The function numbers() takes a string as argument,
# that you can assume is the name of a file that exists
# in the working directory.
#
# The file can contain anywhere any number of blank lines
# (that is, lines containing an arbitrary number of spaces
# and tabs--an empty line being the limiting case).
#
# Nonblank lines are always of the form:
# axb^c
# where a is a nonempty sequence of dots, b is an integer
# and c is a nonempty sequence of dots,
# with no space anywhere on the line,
# that represents
#      (number of dots in a) times (b to the power the number of dots in c)
# For instance, ..x-3^..... represents 2 x (-3 ^ 5), so -486.
# Note that ** is the Python operator for exponentiation.
#
# The function returns the (possibly empty) list of all such "numbers"
# (so there are as many elements in the list as nonempty lines in the file).


def frieze(n):
    # Function to print the frieze pattern
    # Top part
    top = '\\  /' * (n + 1)
    print(top.rstrip())  # Remove trailing space
    
    # Middle part
    middle = ' \\/' + '..\\/' * n
    print(middle.rstrip())
    
    # Bottom part
    bottom = ' || ' * (n + 1)
    print(bottom.rstrip())
    
    # Additional parts
    additional_top = '/' + ' ' * (4 * n + 2) + '\\'
    print(additional_top.rstrip())


def numbers(filename):
    result = []
    
    def process_line(line):
        # Split the line into parts based on 'x' and '^'
        a_part, rest = line.split('x', 1)
        b_part, c_part = rest.split('^', 1)
        
        # Count the number of dots in a and c
        a_dots = len(a_part)
        c_dots = len(c_part)
        
        # Extract the integer b
        b = int(b_part)
        
        # Calculate the number and return it
        return a_dots * (b ** c_dots)
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Process only non-empty lines
                if 'x' in line and '^' in line:
                    result.append(process_line(line))
    
    return result
