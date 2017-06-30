first = 1
second = 1
sum = 0;

print first
print second
for j in range(8):
	sum = first + second
	first = second
	second = sum
	print sum