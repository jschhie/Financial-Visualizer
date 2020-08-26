# DRAFT: Personal Expenses Tracker GUI
# path: vim ~/Desktop/projects/py_study/tk_samples/expenseTracker.py
from tkinter import *


def raise_frame(frame):
    frame.tkraise()


class ExpenseTracker:
    
    def __init__(self, master):
        self.master = master
        
        self.curr_balance = "0"

        self.main_frame = Frame(master)
        self.new_txn_frame = Frame(master)
        self.history_frame = Frame(master)
        
        for f in (self.main_frame, self.new_txn_frame, self.history_frame):
            f.grid(row=0, column=0, sticky="news")

        raise_frame(self.main_frame)
        self.create_main_frame()


    def create_main_frame(self):
        # Show main prompt
        Label(self.main_frame, text="Main Menu").grid(row=0, columnspan=2)

        # Show Current Balance
        Label(self.main_frame, text="Current Balance: ").grid(sticky=E)
        
        self.curr_balance_text = Entry(self.main_frame)
        self.curr_balance_text.insert(END, '$' + self.curr_balance)
        self.curr_balance_text.config(state="disabled")
        self.curr_balance_text.grid(row=1, column=1)

        # Show Available Actions
        Label(self.main_frame, text="Choose an Action: ").grid(row=2, sticky=E)

        # New Transaction Button
        new_txn_button = Button(self.main_frame, text="New Transaction")
        new_txn_button.bind("<Button-1>", self.make_new_txn)
        new_txn_button.grid(row=2, column=1)

        # View History Button
        view_hist_button = Button(self.main_frame, text="View History")
        view_hist_button.bind("<Button-1>", self.view_history)
        view_hist_button.grid(row=3, column=1)
        
        # Quit Button
        quit_button = Button(self.main_frame, text="Quit", command=self.master.quit)
        quit_button.grid(row=4, column=1)


    def make_new_txn(self, event):
        # Show new frame and prompt
        raise_frame(self.new_txn_frame)
        Label(self.new_txn_frame, text="Create New Transaction").grid(row=0, columnspan=2)

        # Amount Label and Entry
        Label(self.new_txn_frame, text="Amount: ").grid(row=1, sticky=E)
        self.user_amount = Entry(self.new_txn_frame)
        self.user_amount.grid(row=1, column=1)

        # Date Label and Entry
        Label(self.new_txn_frame, text="Date (MM/DD/YYYY): ").grid(row=2, sticky=E)
        self.user_date = Entry(self.new_txn_frame)
        self.user_date.grid(row=2, column=1)

        # Determine if Adding or Deducting from Current Balance
        deposit_button = Button(self.new_txn_frame, text="Deposit")
        deposit_button.bind("<Button-1>", self.deposit_money)
        deposit_button.grid(row=3, column=1)

        # Back to Main Menu Button
        back_button = Button(self.new_txn_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=5, column=1)
    

    def deposit_money(self, event):
        # TODO Split curr_balance by '.' decimal delimiter
        # TODO assumes WHOLE numbers for now
        self.curr_balance = str(int(self.curr_balance) + int(self.user_amount.get()))
        pass


    def return_to_main(self, event):
        # TODO Get updated current balance
        self.curr_balance_text.config(state="normal")
        self.curr_balance_text.delete(0, END)
        self.curr_balance_text.insert(END, '$' + self.curr_balance)
        self.curr_balance_text.config(state="disabled")
        raise_frame(self.main_frame)
        pass


    def view_history(self, event):
        print('View History')
        raise_frame(self.history_frame)
        pass


root = Tk()
root.geometry("500x500")
root.title('Personal Expenses Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()
