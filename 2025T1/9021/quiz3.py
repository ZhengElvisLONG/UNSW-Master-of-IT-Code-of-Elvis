import sys

try:
    user_num = int(input('Enter an integer: '))
    if user_num == 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

positive_num = abs(user_num)
result = ''
if positive_num == 0:
    result = '0'
else:
    while positive_num > 0:
        remainder = positive_num % 3
        result = str(remainder) + result
        positive_num = positive_num // 3
print(f'Your input in base 3 reads: {("+" if user_num > 0 else "-")}{result}')
print()  

is_positive = user_num > 0

directions = {
    'North': '⇧',
    'South': '⇩',
    'North West': '⬁',
    'South East': '⬂', 
    'North East': '⬀',
    'South West': '⬃'
}

my_arrows = ''
flipped = result[::-1]
for num in flipped:
    if num == '0':
        if is_positive:
            dir = 'North'
        else:
            dir = 'South'
    elif num == '1':
        if is_positive:
            dir = 'North West'
        else:
            dir = 'South East'
    else:
        if is_positive:
            dir = 'North East'
        else:
            dir = 'South West'
    my_arrows += directions[dir] + ' '
my_arrows = my_arrows.rstrip()
print('This is how we will travel (reading digits from right to left):')
print(my_arrows)
print()

print('This is how we travelled:')

    
indent = 0
min_i = 0
last = ''
if my_arrows[0] in "⬀⇧⬁":
    my_arrows = my_arrows[::-1]

for a in my_arrows:
    if a == ' ':
        continue
    if  (a == '⬁' and last == '⬀'):
        indent = indent - 1
        last = a
        continue
    elif (a == '⬀' and last == '⬁'):
        indent = indent + 1
        last = a
        continue
    if (a == '⬂' and last == '⇩') or (a == '⬂' and last == '⬂') or (a == '⇧' and last == '⬁') or (a == '⬁' and last == '⬁') or (a == '⬂' and last == '⬃'):
        indent = indent + 1
    elif (a == '⇧' and last == '⬀') or (a == '⬀' and last == '⬀') or (a == '⬃' and last == '⬂') or (a == '⬀' and last == '⬁') or (a == '⬃' and last == '⬃') or (a == '⬃' and last == '⇩'):
        indent = indent - 1
        if min_i > indent:
            min_i = indent
    last = a
indent = -min_i

last = ''
for a in my_arrows:
    if a == ' ':
        continue
    if  (a == '⬁' and last == '⬀'):
        indent = indent - 1
        last = a
        print(" " * indent + a)
        continue
    elif (a == '⬀' and last == '⬁'):
        indent = indent + 1
        last = a
        print(" " * indent + a)
        continue
    if (a == '⬂' and last == '⇩') or (a == '⬂' and last == '⬂') or (a == '⇧' and last == '⬁') or (a == '⬁' and last == '⬁') or (a == '⬂' and last == '⬃'):
        indent = indent + 1
    elif (a == '⇧' and last == '⬀') or (a == '⬀' and last == '⬀') or (a == '⬃' and last == '⬂') or (a == '⬀' and last == '⬁') or (a == '⬃' and last == '⬃') or (a == '⬃' and last == '⇩'):
        if indent > 0:
            indent = indent - 1
    print(" " * indent + a)
    last = a