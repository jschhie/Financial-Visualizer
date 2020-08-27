# Personal Expenses Tracker GUI
from tkinter import *
from tkinter import messagebox

import sqlite3 as sqlite


'''
# My TODO List

[] Insert Transaction Records into Database
[] Work on View History
    [] Add View Deposits/Withdrawals Button
        [] Use SQL Queries: View By ... Month, Year, or Tag
        [] Use matlabplot to Plot Graphs 
'''

conn = sqlite.connect('all_expenses.db')

class ExpenseTracker:
    
    def __init__(self, master):
        ''' Initialize ExpenseTracker and open its database. '''
        self.master = master
        self.curr_balance = 0.0

        # Initialize all frames
        self.main_frame = Frame(master)
        self.new_txn_frame = Frame(master)
        self.withdraw_frame = Frame(master)
        self.history_frame = Frame(master)
        
        for f in (self.main_frame, self.new_txn_frame, 
                self.withdraw_frame, self.history_frame):
            f.grid(row=0, column=0, sticky="NEWS")

        self.init_main_frame()
        self.init_new_txn_frame()
        self.init_withdraw_frame()
        self.init_history_frame() # TODO

        # Create/Load SQL Database
        self.init_db()

        self.main_frame.tkraise()


    def init_db(self):
        ''' Creates a new database if it DNE. '''
        #conn = sqlite.connect('all_expenses.db')
        try:
            conn.create(''' CREATE TABLE EXPENSES
                    (TID INTEGER PRIMARY KEY,
                    MONTH INTEGER NOT NULL,
                    DAY INTEGER NOT NULL,
                    YEAR INTEGER NOT NULL,
                    CURR_BALANCE REAL NOT NULL,
                    IS_WITHDRAW INTEGER DEFAULT 0,
                    TAG CHAR(30));
                    ''')
        except:
            print('already created database')
            pass


    def init_main_frame(self):
        ''' Initialize Main Frame. '''
        Label(self.main_frame, text="Main Menu").grid(row=0, columnspan=2)

        # Show Current Balance
        Label(self.main_frame, text="Current Balance: ").grid(sticky=E)

        self.curr_balance_text = Entry(self.main_frame)
        self.curr_balance_text.insert(END, '$' + format(self.curr_balance, '.2f'))
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
        quit_button = Button(self.main_frame, text="Quit")
        quit_button.bind("<Button-1>", self.custom_quit)
        quit_button.grid(row=4, column=1)


    def custom_quit(self, event):
        conn.commit()
        conn.close()
        self.master.quit() # ADDED


    def init_new_txn_frame(self):
        ''' Initialize New Transaction Frame. '''
        Label(self.new_txn_frame, text="Add New Transaction").grid(columnspan=2)

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
    

    def init_withdraw_frame(self):
        ''' Initialize New Frame specifically for Withdrawals. '''
        Label(self.withdraw_frame, text="Select a Tag: ").grid(row=0, sticky=E)

        # Associate withdrawal with a Tag
        tags_listbox = Listbox(self.withdraw_frame, selectmode=BROWSE, height=5)
        tags = ['Shopping', 'Health', 'Food', 'Rent', 'Other']
        for tag in tags:
            tags_listbox.insert(END, tag)

        tags_listbox.bind("<<ListboxSelect>>", self.get_tag)
        tags_listbox.grid(row=0, column=1)


    def init_history_frame(self):
        ''' Initialize View History Frame. '''
        Label(self.history_frame, text="View History").grid(row=0, columnspan=2)
        # TODO
        # Add Viewer Modes: View Deposits, View Withdrawals (by Date/Tag)

        # Back to Main Menu Button
        back_button = Button(self.history_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=1, column=1)
        pass


    def check_txn_input(self, is_deposit_txn):
        ''' Checks for valid amount to deposit/withdraw and valid 
        date entry in (MM/DD/YYYY) format. '''
        try:
            # Check User Amount
            pending_total = float(self.curr_balance)
            pending_change = float(self.user_amount.get())

            # Make sure amount is positive
            assert(pending_change > 0.0)

            enough_funds = True
            if is_deposit_txn:
                pending_total += pending_change
            else:
                # Otherwise, is_withdraw_txn=True
                if pending_total < pending_change:
                    enough_funds = False
                pending_total -= pending_change

            try:
                # Check User Dates
                user_date = self.user_date.get()
                month, day, year = user_date.split('/')
                for date_input in (month, day, year):
                    assert(date_input.isnumeric())

                assert(int(month) <= 12 and int(month) > 0)
                assert(int(day) <= 31 and int(month) > 0)
                assert(int(year) >= 2000 and int(year) <= 2020)

                # Warn user if any insufficient funds
                if (enough_funds == False):
                    messagebox.showwarning('Insufficient Funds', 
                        'Amount to withdraw is greater than current balance.')
                
                # Successful New Transaction (Deposit/Withdraw)
                self.curr_balance = pending_total
                return True

            except:
                messagebox.showerror("Input Error", 
                    "Please use (MM/DD/YYYY) format.\
                    \nYear should be between 2000 and 2020.")
        
        except:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

        # Indicate Failure
        return False

    def add_new_txn(self, event):
        self.new_txn_frame.tkraise()


    def deposit_money(self, event):
        if (self.check_txn_input(is_deposit_txn=True)):
            # Redirect to Main Menu
            deposit_val = format(float(self.user_amount.get()), '.2f')

            messagebox.showinfo('Successful Transaction',
                'Deposit of $%s completed.\nReturning to Main Menu.'
                % deposit_val)

            self.return_to_main(event="<Buttton-1>")
        else:
            # Remain on current Frame
            pass


    def withdraw_money(self, event):
        if (self.check_txn_input(is_deposit_txn=False)):
            self.withdraw_frame.tkraise()
        else:
            # Remain on current Frame
            pass


    def get_tag(self, event):
        widget = event.widget
        if (result_tuple:=widget.curselection()):
            idx = int(result_tuple[0])
            tag_value = widget.get(idx)

            withdraw_val = format(float(self.user_amount.get()), '.2f')
            messagebox.showinfo('Successful Transaction',
                'Withdrawal of $%s for %s completed.\nReturning to Main Menu.' 
                % (withdraw_val, tag_value))

            self.return_to_main(event="<Buttton-1>")


    def view_history(self, event):
        # TODO
        self.history_frame.tkraise()
        pass


    def return_to_main(self, event):
        ''' Returns to Main Frame. '''
        # Get most up-to-date balance
        self.curr_balance_text.config(state="normal")
        self.curr_balance_text.delete(0, END)
        self.curr_balance_text.insert(END, '$' + format(self.curr_balance, '.2f'))
        self.curr_balance_text.config(state="disabled")

        # Clear current contents
        for widget in (self.user_date, self.user_amount):
            widget.delete(0, END)

        # Go to Main Frame
        self.main_frame.tkraise()


# Run Program
root = Tk()
root.geometry("500x500")
root.title('Personal Expenses Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()
