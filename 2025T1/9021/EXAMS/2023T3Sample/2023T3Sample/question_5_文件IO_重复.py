# Will be tested with year between 1913 and 2013.


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
    months = 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',\
             'Sep', 'Oct', 'Nov', 'Dec'
    # INSERT YOUR CODE HERE
    inflation_data = []
    
    with open('cpiai.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['Date']
            current_year = int(date.split('-')[0])
            if current_year == year:
                month_num = int(date.split('-')[1])
                inflation = float(row['Inflation'])
                inflation_data.append((month_num, inflation))
    
    if not inflation_data:
        print(f"In {year}, no inflation data available.")
        return
    
    max_inflation = max(inflation for month_num, inflation in inflation_data)
    max_months_nums = [month_num for month_num, inflation in inflation_data if inflation == max_inflation]
    
    max_months = [months[month_num - 1] for month_num in max_months_nums]
    
    print(f"In {year}, maximum inflation was: {max_inflation}")
    month_str = ', '.join(max_months)
    print(f"It was achieved in the following months: {month_str}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()
