# ----- Personal Expenses Tracker GUI -----
from tkinter import *
from tkinter import messagebox

from helper_lib import *

import sqlite3 as sqlite
import pickle

# Connect application to SQLite DB
conn = sqlite.connect('expenses.db')

class ExpenseTracker:
    
    def __init__(self, master):
        ''' Initialize ExpenseTracker and open its database. '''
        
        self.master = master
        self.results_tuple = () # Stores user input if valid
        
        # Load most up-to-date balance
        try:
            with open('curr_balance.pickle', 'rb') as f:
                self.curr_balance = pickle.load(f)
        except FileNotFoundError:
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
        self.init_history_frame()
        self.init_db()
        
        # Go to Main Menu by default
        self.main_frame.tkraise()


    def init_db(self):
        ''' Creates a new database if it DNE. '''
        try:
            conn.execute(''' CREATE TABLE EXPENSES
                    (TID INTEGER PRIMARY KEY,
                    MONTH INTEGER NOT NULL,
                    DAY INTEGER NOT NULL,
                    YEAR INTEGER NOT NULL,
                    AMOUNT REAL NOT NULL,
                    IS_WITHDRAW INTEGER DEFAULT 0,
                    TAG CHAR(30) DEFAULT NULL);
                    ''')
        except:
            # DB and table already exist
            pass


    def init_main_frame(self):
        ''' Initialize Main Frame. '''
        
        # Show Main Menu and Current Balance
        Label(self.main_frame, text="Main Menu").grid(column=1)
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
        quit_button = Button(self.main_frame, text="Save Changes")
        quit_button.bind("<Button-1>", self.custom_quit)
        quit_button.grid(row=4, column=1)


    def custom_quit(self, event):
        ''' Save current session's transactions and updated balance '''
        conn.commit()
        with open('curr_balance.pickle', 'wb') as f:
            pickle.dump(self.curr_balance, f)
        conn.close()
        self.master.quit()


    def init_new_txn_frame(self):
        ''' Initialize New Transaction Frame. '''
        Label(self.new_txn_frame, text="Add New Transaction").grid(column=1)

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
        
        Label(self.withdraw_frame, text="To continue withdrawal, select a Tag.").grid(column=1)
        Label(self.withdraw_frame, text="Available Tags: ").grid(row=1, sticky=E)

        # Associate withdrawal with a Tag
        tags_listbox = Listbox(self.withdraw_frame, selectmode=BROWSE, height=7)
        tags = ['Shopping', 'Health', 'Food/Drink', 'Bills', 
            'Travel', 'Entertainment', 'Other']
        
        for tag in tags:
            tags_listbox.insert(END, tag)
            
        tags_listbox.bind("<<ListboxSelect>>", self.get_tag)
        tags_listbox.grid(row=1, column=1)


    def init_history_frame(self):
        ''' Initialize View History Frame. '''
        
        Label(self.history_frame, 
            text="Please specify year and month, if applicable.").grid(column=1)
        
        # Add Filter Modes (Year and Month)
        Label(self.history_frame, text="Year (YYYY): ").grid(row=1, sticky=E)
        Label(self.history_frame, text="Month (MM): ").grid(row=2, sticky=E)

        self.year_filter = Entry(self.history_frame)
        self.year_filter.grid(row=1, column=1)
        self.month_filter = Entry(self.history_frame)
        self.month_filter.grid(row=2, column=1)

        view_tags_button = Button(self.history_frame, text="View By Tags")
        view_tags_button.bind("<Button-1>", self.view_by_tag)
        view_tags_button.grid(row=3, column=1)

        view_all_button = Button(self.history_frame, 
            text="View Deposits vs. Withdrawals")
        view_all_button.bind("<Button-1>", self.view_all)
        view_all_button.grid(row=4, column=1)

        view_by_year_button = Button(self.history_frame,
            text="View By Year Only")
        view_by_year_button.bind("<Button-1>", self.view_by_year)
        view_by_year_button.grid(row=5, column=1)

        # Back to Main Menu Button
        back_button = Button(self.history_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=6, column=1)


    def view_by_year(self, event):
        ''' Perform SQL Query to view all Transactions within given year. 
        Group by transaction type (withdrawal/deposits) and month. '''
        
        in_year = self.year_filter.get()
        
        if (len(filters:=check_view_filters(in_year, ignore_month=True)) == 0):
            # Invalid user filters
            return

        # Valid Year given, but may or may not be associated with a record
        user_year, _ = filters
        outputs = conn.execute(''' 
            SELECT SUM(AMOUNT), MONTH, IS_WITHDRAW FROM EXPENSES
            WHERE YEAR == (?)
            GROUP BY MONTH, IS_WITHDRAW ''', (user_year, ))

        # Special case: Not all months will have both types of transactions
        # Example: 
            ## January and March had exclusively deposits while
            ## User did not commit anything during October and December
        # So, initialize total_deposits and total_withdrawals to 0.0 per month
        total_months = 12
        total_deposits = [0.0] * total_months
        total_withdrawals = [0.0] * total_months
        at_least_one_txn = False

        for row in outputs:
            at_least_one_txn = True
            temp_amt = row[0]
            month_digit = row[1]
            is_withdrawal_flag = row[2]
            if is_withdrawal_flag == 1:
                total_deposits[month_digit - 1] = temp_amt
            else:
                total_withdrawals[month_digit - 1] = temp_amt

        if at_least_one_txn == False:
            messagebox.showerror("Query Failure",
                "No existing transactions that fit your query.\
                Please try a different year. ")
            return

        # Otherwise, plot grouped bar chart
        show_bar_chart(total_deposits, total_withdrawals, user_year)


    def view_by_tag(self, event):
        ''' Perform SQL Query to view Transactions, 
        by associated Tag for specified year and month. '''
        
        # Check for valid numeric inputs
        in_year = self.year_filter.get()
        in_month = self.month_filter.get()
        if (len(filters:=check_view_filters(in_year, in_month)) == 0):
            return

        # Otherwise, unpack filters
        user_year, user_month = filters

        outputs = conn.execute(''' 
            SELECT SUM(AMOUNT), TAG FROM EXPENSES
            WHERE YEAR == (?) AND MONTH == (?) AND IS_WITHDRAW == 1
            GROUP BY TAG ''', (user_year, user_month))

        all_amounts = []
        all_tags = []
        for row in outputs: 
            # Each row is a tuple, so unpack values
            temp_amt, temp_tag = row
            all_amounts.append(temp_amt)
            all_tags.append(temp_tag)

        if len(all_amounts) == 0:
            messagebox.showerror("Query Failure",
                "No existing transactions that fit your query.\
                Please try a different year and/or month. ")
            return

        show_plot(exp_values=all_amounts, 
            exp_labels=all_tags,
            u_month=user_month, u_year=user_year)


    def view_all(self, event):
        ''' Perform SQL Query to view all withdrawals versus deposits 
        during specified month and year. '''
        
        in_year = self.year_filter.get()
        in_month = self.month_filter.get()
        
        if (len(filters:=check_view_filters(in_year, in_month)) == 0):
            # Invalid user filters
            return

        # Otherwise, unpack filters
        user_year, user_month = filters

        outputs = conn.execute(''' 
            SELECT SUM(AMOUNT), IS_WITHDRAW FROM EXPENSES
            WHERE YEAR == (?) AND MONTH == (?)
            GROUP BY IS_WITHDRAW ''', (user_year, user_month))

        # Default
        deposits = None
        withdrawals = None

        for i, row in enumerate(outputs):
            if i == 0:
                deposits = row[0]
            elif i == 1:
                withdrawals = row[0]
        
        if deposits is None or withdrawals is None:
            messagebox.showerror("Query Failure",
                "No existing transactions that fit your query.\
                Please try a different year and/or month. ")
            return

        show_plot(exp_values=[deposits, withdrawals], 
            exp_labels=['Deposits', 'Withdrawals'],
            u_month=user_month, u_year=user_year)

    
    def add_new_txn(self, event):
        ''' Redirects to New Transaction Page.'''
        self.new_txn_frame.tkraise()


    def deposit_money(self, event):
        ''' Attempt to deposit requested amount on given date. ''' 
        
        # Collect info from user
        init_total = float(self.curr_balance)
        pending_change = self.user_amount.get()
        user_date = self.user_date.get()

        self.results_tuple = check_txn_input(init_total, pending_change, 
                                            user_date, is_deposit_txn=True)
        
        if len(self.results_tuple) > 0:
            # Unpack the results_tuple and update curr_balance
            self.curr_balance, u_month, u_day, u_year, u_amount = self.results_tuple
            
            # Sucessful deposit, so insert new deposit entry into database
            conn.execute(''' INSERT INTO EXPENSES 
                (MONTH, DAY, YEAR, AMOUNT) \
                VALUES (?, ?, ?, ?)''', (u_month, u_day, u_year, u_amount))
            
            # Indicate successful deposit
            deposit_val = format(u_amount, '.2f')
            messagebox.showinfo('Successful Transaction',
                'Deposit of $%s completed.\nReturning to Main Menu.'
                % deposit_val)
            
            # Redirect to Main Menu
            self.return_to_main(event="<Buttton-1>")
        else: 
            # results_tuple is empty tuple meaning invalid user input
            # Remain on current Frame
            pass


    def withdraw_money(self, event):
        ''' Attempt to withdraw requested amount on given date. '''
        
        # Collect info from user
        init_total = float(self.curr_balance)
        pending_change = self.user_amount.get()
        user_date = self.user_date.get()
        
        self.results_tuple = check_txn_input(init_total, pending_change, 
                                        user_date, is_deposit_txn=False)
        
        if len(self.results_tuple) > 0:
            # Valid input received as results
            self.withdraw_frame.tkraise()
        else:
            # results_tuple is empty tuple meaning invalid user input
            # Remain on current Frame
            pass


    def get_tag(self, event):
        ''' Associates withdrawal transaction with a Tag. '''
        widget = event.widget
        if (selections:=widget.curselection()):
            # Get corresponding Tag
            idx = int(selections[0])
            tag_value = widget.get(idx)
            # Insert new record as withdrawal
            self.curr_balance, u_month, u_day, u_year, u_amount = self.results_tuple
            # Perform SQL Query
            conn.execute(''' INSERT INTO EXPENSES 
               (MONTH, DAY, YEAR, AMOUNT, IS_WITHDRAW, TAG) \
               VALUES (?, ?, ?, ?, 1, ?)''', (u_month, u_day, u_year, u_amount, tag_value))
            # Indicate successful withdrawal
            withdraw_val = format(u_amount, '.2f')
            messagebox.showinfo('Successful Transaction',
                'Withdrawal of $%s for %s completed.\nReturning to Main Menu.' 
                % (withdraw_val, tag_value))
            # Redirect to Main Menu
            self.return_to_main(event="<Buttton-1>")
        else:
            # No entry given
            pass


    def view_history(self, event):
        ''' Redirect to View History Page. '''
        self.history_frame.tkraise()


    def return_to_main(self, event):
        ''' Returns to Main Frame. '''
        
        # Get most up-to-date balance
        self.curr_balance_text.config(state="normal")
        self.curr_balance_text.delete(0, END)
        self.curr_balance_text.insert(END, '$' + format(self.curr_balance, '.2f'))
        self.curr_balance_text.config(state="disabled")
        
        # Clear current contents
        for widget in (self.user_date, self.user_amount, self.year_filter, self.month_filter):
            widget.delete(0, END)
        
        # Redirect to Main Frame
        self.main_frame.tkraise()


# Run ExpensesTracker GUI
root = Tk()
root.geometry("450x200")
root.title('Personal Finance Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()
