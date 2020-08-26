# Personal Expenses Tracker GUI
from tkinter import *
from tkinter import messagebox

class ExpenseTracker:
    
    def __init__(self, master):
        self.master = master
        self.curr_balance = "0"

        # Initialize all frames
        self.main_frame = Frame(master)
        self.new_txn_frame = Frame(master)
        self.history_frame = Frame(master)
        
        for f in (self.main_frame, self.new_txn_frame, self.history_frame):
            f.grid(row=0, column=0, sticky="NEWS")

        self.init_main_frame()
        self.init_new_txn_frame()
        self.init_history_frame() # TODO

        # Display Main Frame by default
        self.main_frame.tkraise()


    def init_main_frame(self):
        # Show Main Menu
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
        new_txn_button.bind("<Button-1>", self.add_new_txn)
        new_txn_button.grid(row=2, column=1)

        # View History Button
        view_hist_button = Button(self.main_frame, text="View History")
        view_hist_button.bind("<Button-1>", self.view_history)
        view_hist_button.grid(row=3, column=1)
        
        # Quit Button
        quit_button = Button(self.main_frame, text="Quit", command=self.master.quit)
        quit_button.grid(row=4, column=1)


    def init_new_txn_frame(self):
        # Show New Transaction Prompt
        Label(self.new_txn_frame, text="Create New Transaction").grid(row=0, columnspan=2)

        # Amount Label and Entry
        Label(self.new_txn_frame, text="Amount: ").grid(row=1, sticky=E)
        self.user_amount = Entry(self.new_txn_frame)
        self.user_amount.grid(row=1, column=1)

        # Date Label and Entry
        Label(self.new_txn_frame, text="Date (MM/DD/YYYY): ").grid(row=2, sticky=E)
        self.user_date = Entry(self.new_txn_frame)
        self.user_date.grid(row=2, column=1)

        # Create Deposit Button
        deposit_button = Button(self.new_txn_frame, text="Deposit")
        deposit_button.bind("<Button-1>", self.deposit_money)
        deposit_button.grid(row=3, column=1)

        # Create Withdraw Button
        withdraw_button = Button(self.new_txn_frame, text="Withdraw")
        withdraw_button.bind("<Button-1>", self.withdraw_money)
        withdraw_button.grid(row=4, column=1)

        # Back to Main Menu Button
        back_button = Button(self.new_txn_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=5, column=1)
    

    def init_history_frame(self):
        # Show View History Prompt
        Label(self.history_frame, text="View History").grid(row=0, columnspan=2)
        # TODO
        # Add Viewer Modes: View Deposits, View Withdrawals (by Date/Tag)

        # Back to Main Menu Button
        back_button = Button(self.history_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=1, column=1)
        pass


    def add_new_txn(self, event):
        self.new_txn_frame.tkraise()
        pass


    def deposit_money(self, event):
        # TODO Split curr_balance by '.' decimal delimiter
        # TODO assumes WHOLE numbers for now
        try:
            self.curr_balance = str(int(self.curr_balance) + int(self.user_amount.get()))
        except:
            messagebox.showerror("Deposit Amount::Input Error", "Please enter a valid amount to deposit.")
            pass


    def withdraw_money(self, event):
        # TODO Handle negative amounts
        try:
            self.curr_balance = str(int(self.curr_balance) - int(self.user_amount.get()))
        except:
            messagebox.showerror("Withdraw Amount::Input Error", "Please enter a valid amount to withdraw.")
            pass


    def view_history(self, event):
        self.history_frame.tkraise()
        pass


    def return_to_main(self, event):
        # Get most up-to-date balance
        self.curr_balance_text.config(state="normal")
        self.curr_balance_text.delete(0, END)
        self.curr_balance_text.insert(END, '$' + self.curr_balance)
        self.curr_balance_text.config(state="disabled")

        # Go to Main Frame
        self.main_frame.tkraise()


# Run Program
root = Tk()
root.geometry("500x500")
root.title('Personal Expenses Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()
