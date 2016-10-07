from dao import ReceivableDao
import operator
from datetime import datetime

class Receivable:

	def __init__(self, row):
		self.id = row['id']
		self.net = row['amount'] - row['fee']
		self.date = datetime.strptime(row['payment_date'], '%Y-%m-%d')


	def __str__(self):
		return str(self.id) + ' ' + str(self.net) + ' ' + str(self.date)


	@classmethod
	def by_forward_date(cls, row, forward_date_str):
		new_object = cls(row)
		new_object.set_charges(forward_date_str)
		return new_object


	def set_charges(self, forward_date_str):
		forward_date = datetime.strptime(forward_date_str, '%Y_%m_%d')
		days_diff = max(0, (self.date - forward_date).days)

		self.back_payment = int((0.57/3000.0) * days_diff * self.net)
		self.gross_income = int((3.14/3000.0) * days_diff * self.net)
		self.net_income = self.gross_income - self.back_payment
		self.for_customer = self.net - self.gross_income


class ReceivableBusiness:

	def __init__(self, thousands, forward_date_str, target, tolerance_rate):
		self.forward_date = datetime.strptime(forward_date_str, '%Y_%m_%d')
		self.dao = ReceivableDao.by_thousands(thousands)
		self.solutions = []
		self.get_rows(forward_date_str)
		self.get_stats()
		self.populate_subset(target, tolerance_rate)
		self.get_most_lucrative_solution()


	def get_rows(self, date_str):
		all_rows = [Receivable.by_forward_date(row, date_str) for row in self.dao.select_all_receivables()]
		all_rows.sort(key = operator.attrgetter('for_customer'))
		self.sorted_rows = all_rows


	def get_stats(self):
		self.max_value = sum(row.for_customer for row in self.sorted_rows if row is not None)
		self.row_map = {row.id : row for row in self.sorted_rows}
		self.row_count = len(self.sorted_rows)


	# Populates the solution subset, if the target is smaller than the receivable sum
	def populate_subset(self, target, tolerance_rate):
		self.target = target
		self.__find_subset(self.sorted_rows, 0, [None for x in range(self.row_count)], 0, target, int(tolerance_rate * target))


	# Recursive method for the method above
	def __find_subset(self, rows, from_index, stack, stack_len, target, tolerance):
		if target > self.max_value:
			return

		if len(self.solutions) is 10:
			return

		if 0 <= target <= tolerance:
			self.solutions.append(stack[0:stack_len])
			return

		while from_index < len(rows) and rows[from_index].for_customer > target:
			from_index += 1

		while from_index < len(rows) and rows[from_index].for_customer <= target:
			stack[stack_len] = rows[from_index].id
			self.__find_subset(rows, from_index + 1, stack, stack_len + 1, target - rows[from_index].for_customer, tolerance)
			from_index += 1


	def get_most_lucrative_solution(self):
		if self.target > self.max_value:
			print "Target value (" + str(self.target) + ") exceeds receivables to come (total sum: " + str(self.max_value) + ")"
			return

		self.order_solutions()
		self.solution_pairs.sort(key = operator.itemgetter(1), reverse = True)
		best_solution = self.solution_pairs[0]

		print("Anticipation for %s:" % self.forward_date.strftime('%d/%m/%Y'))
		print("Max profit: $ %s" % (best_solution[1] / 100.0))
		print("Receivable Ids: %s" % sorted(self.solutions[best_solution[0]]))
		print("Value returned to customer: $ %s" % (best_solution[2] / 100.0))
		print("Distance from target value: $ %s" % ((self.target - best_solution[2]) / 100.0))


	def order_solutions(self):
		self.solution_pairs = []
		for i in range(len(self.solutions)):
			income = 0
			target = 0
			for index in self.solutions[i]:
				income += self.row_map[index].net_income
				target += self.row_map[index].for_customer
			self.solution_pairs.append((i, income, target))

