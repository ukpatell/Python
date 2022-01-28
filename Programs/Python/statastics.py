# Finding Stand Deviation from the given list of numbers

import math


def ans(list):
	count = 0
	for x in list:
		answer = (x - 181.46)
		answer =round((answer*answer),2)
		count += answer
	variance = round(count/(len(list)-1),2)
	deviation= math.sqrt(variance)
	print('Values             : ', list)
	print('Total Values       : ', len(list))
	print('Count              : ', count)
	print("Variance           : ", variance)
	print("Standard Deviation : ", deviation)


list = [154.25,173.25,154,184.75,184.25,184.25,210.25,181,176,191,198.25,186.25]

ans(list)

