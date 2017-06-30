from PiStorms import PiStorms
psm = PiStorms()

# def fib(n):
# 	if (n<=2):
# 		return 1
# 	else:
# 		return fib(n-1) + fib(n-2)

# for i in range(10):
# 	psm.screen.termPrintln(fib(i+1))
i=0
up = True
while not psm.isKeyPressed():
	if psm.BAS1.isTouchedEV3():

		if up:
			i+=1
			psm.screen.termPrintln(i)
		up=False
	else:
		up = True
