import sqlite3

class ReceivableDao:

	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()


	@classmethod
	def by_thousands(cls, count):
		if count not in set(['1', '10', '30']):
			raise ValueError('Database ' + count + '_000.sqlite3 does not exist in folder sql/')

		new_object = cls('../sql/' + count + '_000.sqlite3')
		return new_object


	def select_all_receivables(self):
		return self.cursor.execute('SELECT id, amount, fee, payment_date FROM receivables')
