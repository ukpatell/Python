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
print('Solution #2: \n')
printall(mylist)

# Problem 3. Write a Python function kalkul(n) to calculate the following summation for non-negative integer values
# of n:

