from business import ReceivableBusiness

def anticipate(thousands, forward_date_str, target, tolerance_rate):
	ReceivableBusiness(thousands, forward_date_str, target, tolerance_rate)

#anticipate('1', '2016_08_16', 0, 0.001)
#anticipate('1', '2016_08_16', 50000, 0.001)
#anticipate('1', '2016_08_16', 20000000, 0.001)
#anticipate('1', '2016_08_16', 50000000, 0.001)

def fib(n):
	if n < 0:
		return

	if n == 0:
		return 1

	if n == 1:
		return 1

	return fib(n-1) + fib(n-2)

print fib(1000)