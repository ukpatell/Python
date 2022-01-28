def printall(mylist):
	i = 0
	while (i < len(mylist)):
		j = 0
		while (j < len(mylist[i])):
			print(mylist[i][j])
			j+=1
		i+=1


mylist = [ [1,2], [3,4,5], [6,7,8,9]]

printall(mylist)
