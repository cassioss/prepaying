from business import ReceivableBusiness


def anticipate(thousands, forward_date_str, target, tolerance_rate):
	ReceivableBusiness(thousands, forward_date_str, target, tolerance_rate)

anticipate('30', '2016_08_16', 50000, 0.001)