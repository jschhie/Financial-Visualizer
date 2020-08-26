# DRAFT: Personal Expenses Tracker GUI
# path: vim ~/Desktop/projects/py_study/tk_samples/expenseTracker.py
from tkinter import *

class ExpenseTracker:
	
	def __init__(self, master):
		self.master = master
		
		self.prompt_frame = Frame(master)
		self.prompt_frame.pack()

		self.curr_balance_frame = Frame(master)
		self.curr_balance_frame.pack()
		self.curr_balance = "0.00"

		self.bottom_frame = Frame(master)
		self.bottom_frame.pack()
		
		self.show_main_menu()


	def show_main_menu(self):
		# Show Prompt
		prompt = Label(self.prompt_frame, text="Select an Action Below")
		prompt.grid(columnspan=2)

		# Show Current Balance
		curr_balance_lab = Label(self.curr_balance_frame, text="Current Balance: ")
		curr_balance_lab.grid(sticky=E)
		
		curr_balance_text = Entry(self.curr_balance_frame)
		curr_balance_text.insert(END, '$' + self.curr_balance)
		curr_balance_text.config(state="disabled")
		curr_balance_text.grid(row=0, column=1)

		# Show Available Actions
		action_lab = Label(self.bottom_frame, text="Choose Action: ")
		action_lab.grid(row=1, sticky=E)

		# Show Buttons
		## New Transaction
		new_txn_button = Button(self.bottom_frame, text="New Transaction")
		new_txn_button.bind("<Button-1>", self.make_new_txn)
		new_txn_button.grid(row=0, column=1, sticky=W)
		## View History
		view_hist_button = Button(self.bottom_frame, text="View History")
		view_hist_button.bind("<Button-1>", self.view_history)
		view_hist_button.grid(row=1, column=1, sticky=W)

		quit_button = Button(self.bottom_frame, text="Quit", command=self.master.quit)
		quit_button.grid(row=2, column=1, sticky=W)


	def make_new_txn(self, event):
		print('Create New Transaction')
		pass


	def view_history(self, event):
		print('View History')
		pass



root = Tk()
root.geometry("500x500")
root.title('Personal Expenses Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()