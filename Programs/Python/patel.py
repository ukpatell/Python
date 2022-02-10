# Problem 2 : Write a Python procedure printall(list) to print all elements in a list of lists,
# 			  with each element on its own line. For example, if

#   		  mylist = [ [1,2], [3,4,5], [6,7,8,9] ]

# 			  then

#   		  printall(mylist)

# would print the numbers 1-9 on consecutive lines.

# noinspection PyShadowingNames
def printall(mylist):
    i = 0
    while i < len(mylist):
        j = 0
        while j < len(mylist[i]):
            print(mylist[i][j])
            j += 1
        i += 1


mylist = [[1, 2], [3, 4, 5], [6, 7, 8, 9]]
print('Solution #2:')
printall(mylist)


# Problem 3. Write a Python function kalkul(n) to calculate the following summation for non-negative integer values
# of n:

def problem3():
    print('\nSolution #3:\nPlease enter the values for the given formula below:\n')
    print('\t\t n     i       n + 1 ')
    print('\t\t Σ  ------- +  ----- ')
    print('\t\ti=1  i + 1     n + 2 \n')


# noinspection SpellCheckingInspection
def kalkul(value):
    i = 1  # Variable made to be consistent with the formula
    summation = 0  # Update sum for each calculation
    while i <= value:  # n gets incremented each iteration
        answer = ((i / (i + 1)) + (value + 1) / (value + 2))  # calculating sum formula
        summation += answer  # Current sum is added to the total
        i += 1  # incrementation
    return round(summation, 2)


problem3()
n = int(input("Enter [non-negative] value for n: "))

while n < 0:  # Input validation
    n = int(input("Enter [non-negative] value for n: "))

if n == 0:
    print('\nAnswer\t: 0.5')
else:
    print('\nAnswer\t: ', kalkul(n))


# Problem 4. Write a Python function dsum(n) to calculate the following summation for non-negative integer values of n:
def problem4():
    print('\nSolution #4:\nPlease enter the values for the given formula below:\n')
    print('\t\t n    n  ')
    print('\t\t Σ    Σ  3i')
    print('\t\ti=1  j=1\n')


def dsum(val):
    sum = 0
    for x in range(1,val+1):
        currNum = x
        for y in range(1,val+1):
            answer = 3 * currNum
            sum += answer

    return sum


problem4()
n_3 = int(input("Enter [non-negative] value for n: "))

while n_3 < 0:  # Input validation
    n_3 = int(input("Enter [non-negative] value for n: "))

if n_3 == 0:
    print('\nAnswer\t: 0')
else:
    print('\nAnswer\t: ', dsum(n_3))
