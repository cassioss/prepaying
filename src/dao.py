import sqlite3
import operator
from datetime import datetime

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

class CustomerReceivables:
	def __init__(self, filename, date_str, target):
		self.target = target
		self.forward_date = datetime.strptime(date_str, '%Y_%m_%d')
		self.first_solutions = []
		self.db_to_row(filename, date_str)
		if target <= self.max_value:
			self.row_count = len(self.sorted_rows)
			self.populate_subset(self.sorted_rows, 0, [None for x in range(self.row_count)], 0, target, int(0.001 * target))
			self.order_solutions()
		self.get_most_lucrative_solution()

	def db_to_row(self, filename, date_str):
		con = sqlite3.connect('../sql/' + filename + '_000.sqlite3')
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		all_rows = [Receivable.by_forward_date(row, date_str) for row in cur.execute('SELECT id, amount, fee, payment_date FROM receivables')]
		all_rows.sort(key=operator.attrgetter('for_customer'))
		self.sorted_rows = all_rows
		self.row_map = {row.id : row for row in self.sorted_rows}
		self.max_value = sum(row.for_customer for row in self.sorted_rows)

	def populate_subset(self, rows, from_index, stack, stack_len, target, tolerance):
		if len(self.first_solutions) is 10:
			return

		if 0 <= target <= tolerance:
#			print target, tolerance, stack[0:stack_len]
			self.first_solutions.append(stack[0:stack_len])
			return

		while from_index < len(rows) and rows[from_index].for_customer > target:
			from_index += 1

		while from_index < len(rows) and rows[from_index].for_customer <= target:
			stack[stack_len] = rows[from_index].id
			self.populate_subset(rows, from_index + 1, stack, stack_len + 1, target - rows[from_index].for_customer, tolerance)
			from_index += 1

	def order_solutions(self):
		self.solution_pairs = []
		for i in range(len(self.first_solutions)):
			income = 0
			target = 0
			for index in self.first_solutions[i]:
				income += self.row_map[index].net_income
				target += self.row_map[index].for_customer
			self.solution_pairs.append((i, income, target))

	def get_most_lucrative_solution(self):
		if self.target > self.max_value:
			print "Target value (" + str(self.target) + ") exceeds receivables to come (total sum: " + str(self.max_value) + ")"
			return

		self.solution_pairs.sort(key=operator.itemgetter(1), reverse=True)
		best_solution = self.solution_pairs[0]
		print("Anticipation for %s:" % self.forward_date.strftime('%d/%m/%Y'))
		print("Max profit: $ %s" % (best_solution[1] / 100.0))
		print("Receivable Ids: %s" % sorted(self.first_solutions[best_solution[0]]))
		print("Distance from target value: $ %s" % ((self.target - best_solution[2]) / 100.0))

CustomerReceivables('1', '2016_08_16', 500000000)
