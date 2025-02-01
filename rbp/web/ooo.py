def get_int_coos(coos):
	x = coos[1]
	column = int(x) - 1
	y = coos[0]
	row = 0 if y=="G" else (1 if y=="F" else (2 if y=="E" else (3 if y=="D" else (4 if y=="C" else (5 if y=="B" else (6 if y=="A" else -1))))))
	return row, column

print(get_int_coos("G1"))
print(get_int_coos("F3"))
