class BankIpotec(object):
	"""
	Ипотечный калькулятор - Рассчитайте ежемесячные платежи по срочным ипотечным 
	кредитам за указанные N-е условия по заданной процентной ставке Также выясните, 
	сколько времени потребуется пользователю для возврата кредита, необязательный параметр
	первоначальный сумма первоначального взноса.
	
	summa: сумма ипотеки: int
	period: педиод на который берется кредит (лет): int
	proc: процентная ставка банка: float
	first_pay: сумма первоначальноего платежа: int
	"""
	def __init__(self, summa, period, proc, first_pay=0):
		""" инит класа """
		self.summa = summa
		self.period = period
		self.proc = proc
		self.first_pay = first_pay

	def diff_pay_list(self):
		"""
		Функция рассчета дифференцированных платежей

		return: (список платежей:list, сумма выплат за период:int): tuple
		"""
		m_period = self.period * 12
		sum_bank = self.summa - self.first_pay
		pay_mounth = sum_bank / m_period
		pay_list = []

		while m_period != 0:
			pm = pay_mounth + (sum_bank * self.proc / 1200)
			pay_list.append(round(pm, 2))
			sum_bank -= pay_mounth
			m_period -= 1
		return pay_list, round(sum(pay_list), 2)

	def ann_pay(self):
		"""
		Функция рассчета аннуитетных платежей 

		return: (платежи в месяц:int, сумма всех выплат за период:int): tuple
		"""
		m_period = self.period * 12
		prcnt = self.proc / 1200.0
		ann_k = (prcnt * (1 + prcnt) ** m_period) / (((1 + prcnt) ** m_period) - 1)
		pm = (self.summa - self.first_pay) * ann_k
		total_pay = pm * m_period
		return round(pm, 2), round(total_pay, 2)



ipotec = BankIpotec(1000000, 10, 15)
print(ipotec.ann_pay())

		