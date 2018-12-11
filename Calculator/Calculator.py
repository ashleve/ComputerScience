import tkinter as tk
from decimal import Decimal


class Calculator(tk.Tk):

	args = []	# looks like this: [12419, '+', 902, '/', 0, '-', ...] 
	current = 0
	reset = True

	def __init__(self):
		super().__init__()
		self.title('Calculator')
		self.center_window()
		self.resizable(False, False)
		self.spawn_some_shit()


	def add_digit(self, digit_str):
		if self.reset == True:
			self.reset_all()

		# prevent user from adding digits when there's no place on the screen
		length = len(str(self.current))
		if length > 13:
			return

		self.current *= 10
		self.current += int(digit_str)
		print(self.current)
		self.update_current_display()
		self.reset = False


	def delete_digit(self):
		string = str(self.current)
		if len(string)>1:
			string = string[:-1]
		else:
			string = '0'
		if string.find(',') != -1:
			self.current = float(string)
		else:
			self.current = int(string)
		print(self.current)
		self.update_current_display()


	def update_current_display(self):
		if len(str(self.current)) > 14:
			string = '%.8E' % Decimal(str(self.current))	# scientific notation
			self.display_current['text'] = string
		else:
			self.display_current['text'] = self.current


	def update_args_display(self):
		string = ""
		for arg in self.args:
			string += str(arg)
		self.display_args['text'] = string


	def reset_current(self):
		self.current = 0
		self.display_current['text'] = ""
		

	def reset_args(self):
		self.args.clear()
		self.update_args_display()

	def reset_all(self):
		self.reset_current()
		self.reset_args()


	def operation(self, op):
		if op not in ['+','-', '*', '/', '=', '~']:
			return
		elif op == '=':
			self.calculate()
			self.reset = True
		elif op == '~':
			self.current *= -1
			self.update_current_display()
		else:
			self.args.append(self.current)
			self.args.append(op)
			self.reset_current()
			self.update_args_display()
		if op != '=' and op != '~':
			self.reset = False


	def calculate(self):
		tmp = self.current
		self.current = 0
		last_op = '+'

		for arg in self.args:
			if type(arg) != str:
				if type(arg) == float:
					number = float(arg)
				else:
					number = int(arg)
				try:
					self.execute_operation(number, last_op)
				except ZeroDivisionError:
					self.reset_all()
					self.display_current['text'] = "Nie dziel przez 0 dzbanie"
			else:
				last_op = arg

		try:
			self.execute_operation(tmp, last_op)
			self.reset_args()
			self.update_current_display()
		except ZeroDivisionError:
			self.reset_all()
			self.display_args['text'] = "Nie dziel przez 0 dzbanie"


	def execute_operation(self, number, op):
		if op == '+':
			self.current += number
		elif op == '-':
			self.current -= number
		elif op == '*':
			self.current *= number
		elif op == '/':
			self.current /= number



	def spawn_some_shit(self):
		self.display_args = tk.Label(self, bg='white', text='', font=(None, 15), anchor='e')
		self.display_args.pack(fill=tk.X)

		self.display_current = tk.Label(self, bg='white', text='0', font=(None, 30), anchor='e')
		self.display_current.pack(fill=tk.X)

		self.main_frame = tk.Frame(self, bg='#F2F2F2')	# contener for all buttons
		self.main_frame.pack(side=tk.BOTTOM)


		#------------------ Setting Columns ------------------#

		self.column1 = tk.Frame(self.main_frame, bg='white')
		self.column2 = tk.Frame(self.main_frame, bg='white')
		self.column3 = tk.Frame(self.main_frame, bg='white')
		self.column4 = tk.Frame(self.main_frame, bg='white')
		
		self.column1.pack(side='left')
		self.column2.pack(side='left')
		self.column3.pack(side='left')
		self.column4.pack(side='left')



		#------------------ Setting Buttons ------------------#

		# row1
		squared = self.set_button('x²', self.column3, '#E6E6E6')
		root = self.set_button('√', self.column2, '#E6E6E6')
		modulo = self.set_button('%', self.column1, '#E6E6E6')

		# row2
		delete = self.set_button('del', self.column3, '#E6E6E6')
		C = self.set_button('C', self.column2, '#E6E6E6')
		CE = self.set_button('CE', self.column1, '#E6E6E6')

		# row 3,4,5
		f = (None, 10, 'bold')
		num9 = self.set_button('9', self.column3, font=f)
		num8 = self.set_button('8', self.column2, font=f)
		num7 = self.set_button('7', self.column1, font=f)
		num6 = self.set_button('6', self.column3, font=f)
		num5 = self.set_button('5', self.column2, font=f)
		num4 = self.set_button('4', self.column1, font=f)
		num3 = self.set_button('3', self.column3, font=f)
		num2 = self.set_button('2', self.column2, font=f)
		num1 = self.set_button('1', self.column1, font=f)

		# row 6
		comma = self.set_button('.', self.column3, '#E6E6E6', font=f)	# doesn't work yet
		num0 = self.set_button('0', self.column2, font=f)
		negate = self.set_button('~', self.column1, '#E6E6E6')

		# column 4
		opposite = self.set_button('1/x', self.column4, '#E6E6E6')
		divide = self.set_button('/', self.column4, '#E6E6E6')
		multiply = self.set_button('*', self.column4, '#E6E6E6')
		minus = self.set_button('-', self.column4, '#E6E6E6')
		plus = self.set_button('+', self.column4, '#E6E6E6')
		equals = self.set_button('=', self.column4, '#E6E6E6')


	def set_button(self, text="", parent=None, background='white', font=(None, 10)):
		button = tk.Button(parent)

		button['text'] = text
		button['bg'] = background
		button['font'] = font

		if text.isdigit():
			button['command'] = lambda: self.add_digit(text)
		elif text == 'CE':
			button['command'] = lambda: self.reset_all()
		elif text == 'C':
			button['command'] = lambda: self.reset_current()
		elif text == 'del':
			button['command'] = lambda: self.delete_digit()
		else:
			button['command'] = lambda: self.operation(text)

		button.config(
			height=2, 
			width=7, 
			borderwidth=1, 
			padx=10, 
			pady=5,
			relief='groove',
		)
		button.pack()
		return button


	def center_window(self):
		w = 320
		h = 471

		sw = self.winfo_screenwidth()
		sh = self.winfo_screenheight()
		
		x = (sw - w)/2
		y = (sh - h)/2
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))



def main():
	calc = Calculator()
	calc.mainloop()


if __name__ == '__main__':
	main()
