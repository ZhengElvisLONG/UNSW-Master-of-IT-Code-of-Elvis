# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 5


'''
Will be tested with year between 1913 and 2013.
You might find the reader() function of the csv module useful,
but you can also use the split() method of the str class.
'''

import csv

def f(year):
    '''
    >>> f(1914)
    In 1914, maximum inflation was: 2.0
    It was achieved in the following months: Aug
    >>> f(1922)
    In 1922, maximum inflation was: 0.6
    It was achieved in the following months: Jul, Oct, Nov, Dec
    >>> f(1995)
    In 1995, maximum inflation was: 0.4
    It was achieved in the following months: Jan, Feb
    >>> f(2013)
    In 2013, maximum inflation was: 0.82
    It was achieved in the following months: Feb
    '''
    months = 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    # Insert your code here
    max_value = None
    with open('cpiai.csv') as csvfile:
        for line in csvfile:
            if line.startswith("Date"):
                continue
            else:
                whole_date, index, inflation = line.split(',')
                year_num, mon_num, day_num = whole_date.split('-')
                if year_num == str(year):
                    if max_value is None:
                        max_value = float(inflation)
                    else:
                        max_value = max(max_value, float(inflation))
    L = []
    with open('cpiai.csv') as csvfile:
        for line in csvfile:
            if line.startswith("Date"):
                continue
            else:
                whole_date, index, inflation = line.split(',')
                year_num, mon_num, day_num = whole_date.split('-')
                if year_num == str(year) and float(inflation) >= max_value:
                    L.append(months[int(mon_num) - 1])
    print(f'In {year}, maximum inflation was: {max_value}')
    print(f'It was achieved in the following months: {", ".join(L)}')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
