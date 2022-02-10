# Finding Stand Deviation from the given list of numbers

import math


def ans(list):
	count = 0
	for x in list:
		answer = (x - 5.64)
		temp = answer
		answer =round((answer*answer),2)
		print(f"X: {x}  --- (X-Xbar): {round(temp,2)}, --- (X-Xbar)^2: {answer}")
		count += answer
	variance = round(count/(len(list)-1),2)
	deviation= math.sqrt(variance)
	print('Values             : ', list)
	print('Total Values       : ', len(list))
	print('Count              : ', count)
	print("Variance           : ", variance)
	print("Standard Deviation : ", deviation)

def mean(list):
	count = 0
	for x in list:
		count += x
	print("Sum  : ", count)
	print("Count: ", len(list))
	print("___________________")
	print("Mean: ", count/len(list))


# list = [154.25,173.25,154,184.75,184.25,184.25,210.25,181,176,191,198.25,186.25]
list = [2  ,3 ,  3,   4,   4,   4,   5,   7,   8,   10,   12]

ans(list)
mean(list)
