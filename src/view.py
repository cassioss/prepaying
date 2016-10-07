from business import ReceivableBusiness

def anticipate(thousands, forward_date_str, target, tolerance_rate):
	ReceivableBusiness(thousands, forward_date_str, target, tolerance_rate)

anticipate('1', '2016_08_16', 0, 0.001)
anticipate('1', '2016_08_16', 50000, 0.001)
anticipate('1', '2016_08_16', 23805449, 0.001)
anticipate('1', '2016_08_16', 50000000, 0.001)