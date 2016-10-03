import sqlite3
import operator
from datetime import datetime

class CustomerReceivables:
	def __init__(self, rows):
		self.rows = sorted(rows, key = operator.attrgetter('for_customer'))

class Receivable:
	def __init__(self, row):
		self.id = row['id']
		self.net = row['amount'] - row['fee']
		self.date = datetime.strptime(row['payment_date'], '%Y-%m-%d')

	@classmethod
	def by_forward_date(cls, row, forward_date_str):
		new_object = cls(row)
		new_object.set_charges(forward_date_str)
		return new_object

	def __str__(self):
		return str(self.id) + ' ' + str(self.net) + ' ' + str(self.date)

	def set_charges(self, forward_date_str):
		forward_date = datetime.strptime(forward_date_str, '%Y_%m_%d')
		days_diff = max(0, (self.date - forward_date).days)

		self.back_payment = int((0.57/3000.0) * days_diff * self.net)
		self.gross_income = int((3.14/3000.0) * days_diff * self.net)
		self.net_income = self.gross_income - self.back_payment
		self.for_customer = self.net - self.gross_income

def db_to_row(filename, date_str):
	con = sqlite3.connect('../sql/' + filename + '_000.sqlite3')
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	all_rows = [Receivable.by_forward_date(row, date_str) for row in cur.execute('SELECT id, amount, fee, payment_date FROM receivables')]
	return sorted(all_rows, key=operator.attrgetter('for_customer'))


def subsetSum(rows, n, sum):
	solution_arrays [[0 for x in range()]]
	array = [1] + [0 for x in range(sum)]
	for row in rows:
		for num in xrange(sum - row.for_customer, -1, -1):
			if array[num]:
				array[num + row.for_customer] += array[num]
	return array[sum]


print subsetSum(db_to_row('30', '2016_08_16'), 30000, 50000)



