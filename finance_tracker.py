# ----- Financial Graphic User Interface (GUI) Application -----
from tkinter import *
from tkinter import messagebox

from helper_lib import *

from init_frames import * 

import sqlite3 as sqlite
import pickle

# Connect application to SQLite DB
conn = sqlite.connect('expenses.db')



class ExpenseTracker:
    ###############################################################
    # DEFINE & INITIALIZE EXPENSETRACKER 
    ###############################################################
    def __init__(self, master):
        ''' Initialize ExpenseTracker and open its database. '''
        self.master = master
        self.results_tuple = () 
        try:
            with open('curr_balance.pickle', 'rb') as f:
                self.curr_balance = pickle.load(f)
        except FileNotFoundError:
            self.curr_balance = 0.0

        self.main_frame = Frame(master)
        self.new_txn_frame = Frame(master)
        self.withdraw_frame = Frame(master)
        self.visualize_frame = Frame(master)
        self.history_frame = Frame(master)
        self.summary_frame = Frame(master)

        for f in (self.main_frame, self.new_txn_frame, 
                self.withdraw_frame, self.visualize_frame, 
                self.history_frame, self.summary_frame):
            f.grid(row=0, column=0, sticky="NEWS")

        self.init_main_frame()
        self.init_new_txn_frame()
        self.init_withdraw_frame()
        self.init_visualize_frame()
        self.init_history_frame()
        self.init_summary_frame()

        self.init_db()
        self.main_frame.tkraise()


    ###############################################################
    # INITIALIZE DATABASE & FRAMES 
    ###############################################################
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
        except: # DB and table already exist
            pass

    def init_main_frame(self):
        init_main(root=self)

    def init_new_txn_frame(self):
        init_new_txn(root=self)

    def init_withdraw_frame(self):
        init_withdraw(root=self)

    def init_visualize_frame(self):
        init_visualize(root=self)

    def init_history_frame(self):
        init_history(root=self)

    def init_summary_frame(self):
        init_summary(root=self)

    ###############################################################
    # ACTIVATE QUIT & SAVE BUTTON
    ###############################################################
    def custom_quit(self, event):
        ''' Save current session's transactions and updated balance '''
        conn.commit()
        with open('curr_balance.pickle', 'wb') as f:
            pickle.dump(self.curr_balance, f)
        conn.close()
        self.master.quit()

    ###############################################################
    # VIEW HISTORY FEATURE
    ###############################################################
    def view_history(self, event):
        ''' Redirect to View History Page. '''
        self.history_frame.tkraise()
        return


    def show_summary(self, event):
        ''' Perform SQL Query to show first K Transactions 
        within given month and year. '''
        in_year = self.hist_year_filter.get()
        in_month = self.hist_month_filter.get()
        if (len(filters:=check_view_filters(in_year, in_month)) == 0):
            return # Invalid filters

        global user_year
        global user_month
        user_year, user_month = filters
        
        # Cursor instance is re-used when 'Show More Records' button is clicked
        global cursor
        cursor = conn.execute('''
            SELECT AMOUNT, DAY, TAG FROM EXPENSES
            WHERE YEAR == (?) AND MONTH == (?)
            ORDER BY DAY ''', (user_year, user_month))
        
        self.summary_frame.tkraise()
        self.output_rows()
        return


    def show_more_records(self, event): 
        ''' Called when 'Show More Records' button is clicked. Displays additional records. '''
        # Sets show_more flag to True: Overwrites and erases extra rows from previous query
        self.output_rows(show_more=True)
        return


    def output_rows(self, show_more=False):
        ''' Helper function to display remaining data records. 
        show_more: if output_rows() was called by show_more_records() '''
        global cursor
        global user_year
        global user_month
        
        limit = 10 # Limit number of rows shown at once
        records = cursor.fetchmany(limit)
        numToOverwrite = len(records)
        
        if (numToOverwrite):
            for r, record in enumerate(records): # r rows (starts from index 0)
                for c in range(3): # 3 cols selected
                    summ_entry = Entry(self.summary_frame, width=20)
                    data = record[c]
                    if c == 0:
                        data = '$' + format(record[c], '.2f')
                    elif c == 1:
                        data = str(user_month) + '/' + str(record[c]) + '/' + str(user_year)
                    elif data is None: # Tag DNE for Deposits
                        data = "Deposit"
                    summ_entry.insert(END, data)
                    summ_entry.config(state="disabled")
                    summ_entry.grid(row=r+3, column=c) # +3 as headers takes up first 3 rows
            
            # Check if need to erase previous rows 
            if (show_more): 
                self.erase_previous_rows(offset=numToOverwrite)
        else:
            messagebox.showerror("Error", "No more remaining records to be shown for given date range.")
            return


    def erase_previous_rows(self, offset):
        numToErase = 10 - offset
        i = 0
        startPos = offset + 3 # +3 as headers takes up first 3 rows
        while (numToErase):
            for c in range(3):
                summ_entry = Entry(self.summary_frame)
                summ_entry.insert(END, "")
                summ_entry.config(state="disabled")
                summ_entry.grid(row=startPos+i, column=c)
            numToErase -= 1
            i += 1
        return

 
    ###############################################################
    # VISUALIZE TRANSACTIONS FEATURE
    ###############################################################
    def visualize_txn(self, event):
        ''' Redirect to Visualize Transactions Page. '''
        self.visualize_frame.tkraise()
        return


    def view_by_year(self, event):
        ''' Perform SQL Query to visualize all Transactions within given year. 
        Group by transaction type (withdrawal/deposits) and month. '''
        
        in_year = self.year_filter.get()
        if (len(filters:=check_view_filters(in_year, ignore_month=True)) == 0):
            return # Error: Invalid user filters given

        user_year, _ = filters
        cursor = conn.execute(''' 
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
        
        records = cursor.fetchall()
        if (len(records) == 0):
            messagebox.showerror("Query Failure",
                "No existing transactions that fit your query.\
                Please try a different year. ")
            return

        for row in records:
            at_least_one_txn = True
            temp_amt = row[0]
            month_digit = row[1]
            # Determine if txn is a withdrawal or deposit type
            is_withdrawal_flag = row[2]
            if is_withdrawal_flag == 1:
                total_withdrawals[month_digit - 1] = temp_amt
            else:
                total_deposits[month_digit - 1] = temp_amt
        show_year_chart(total_deposits, total_withdrawals, user_year)
        

    def view_by_tag(self, event):
        ''' Perform SQL Query to view Transactions, 
        by associated Tag for specified year and month. '''

        in_year = self.year_filter.get()
        in_month = self.month_filter.get()
        
        if (len(filters:=check_view_filters(in_year, in_month)) == 0):
            return
        
        user_year, user_month = filters
        cursor = conn.execute(''' 
            SELECT SUM(AMOUNT), TAG FROM EXPENSES
            WHERE YEAR == (?) AND MONTH == (?) AND IS_WITHDRAW == 1
            GROUP BY TAG ''', (user_year, user_month))
        
        all_amounts = []
        all_tags = []
        for row in cursor: 
            temp_amt, temp_tag = row # Each row is a tuple, so unpack values
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
            return
        
        user_year, user_month = filters
        cursor = conn.execute(''' 
            SELECT SUM(AMOUNT), IS_WITHDRAW FROM EXPENSES
            WHERE YEAR == (?) AND MONTH == (?)
            GROUP BY IS_WITHDRAW ''', (user_year, user_month))

        deposits = None
        withdrawals = None
        for i, row in enumerate(cursor):
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


    ###############################################################
    # ADD NEW TRANSACTION FEATURE: DEPOSITS & WITHDRAWALS
    ###############################################################
    def add_new_txn(self, event):
        ''' Redirects to New Transaction Page.'''
        self.new_txn_frame.tkraise()


    def deposit_money(self, event):
        ''' Attempt to deposit requested amount on given date. ''' 

        init_total = float(self.curr_balance)
        pending_change = self.user_amount.get()
        user_date = self.user_date.get()

        # Initializes ExpenseTracker::results_tuple variable
        self.results_tuple = check_txn_input(init_total, pending_change, 
                                            user_date, is_deposit_txn=True)
        if len(self.results_tuple) > 0:
            # Unpack the results_tuple and update curr_balance
            self.curr_balance, u_month, u_day, u_year, u_amount = self.results_tuple
            conn.execute(''' INSERT INTO EXPENSES 
                (MONTH, DAY, YEAR, AMOUNT) \
                VALUES (?, ?, ?, ?)''', (u_month, u_day, u_year, u_amount))
            deposit_val = format(u_amount, '.2f')
            messagebox.showinfo('Successful Transaction',
                'Deposit of $%s completed.\nReturning to Main Menu.'
                % deposit_val)
            self.return_to_main(event="<Buttton-1>")
        else: # Remain on current Frame
            pass


    def withdraw_money(self, event):
        ''' Attempt to withdraw requested amount on given date. '''
        init_total = float(self.curr_balance)
        pending_change = self.user_amount.get()
        user_date = self.user_date.get()
        
        # Initializes ExpenseTracker::results_tuple variable
        self.results_tuple = check_txn_input(init_total, pending_change, 
                                        user_date, is_deposit_txn=False)
        if len(self.results_tuple) > 0:
            self.withdraw_frame.tkraise()
        else: # Remain on current Frame
            pass


    def get_tag(self, event):
        ''' Associates withdrawal transaction with a Tag. '''
        
        widget = event.widget
        if (selections:=widget.curselection()):
            # Get corresponding Tag
            idx = int(selections[0])
            tag_value = widget.get(idx)
            self.curr_balance, u_month, u_day, u_year, u_amount = self.results_tuple

            conn.execute(''' INSERT INTO EXPENSES 
               (MONTH, DAY, YEAR, AMOUNT, IS_WITHDRAW, TAG) \
               VALUES (?, ?, ?, ?, 1, ?)''', (u_month, u_day, u_year, u_amount, tag_value))
            
            withdraw_val = format(u_amount, '.2f')
            messagebox.showinfo('Successful Transaction',
                'Withdrawal of $%s for %s completed.\nReturning to Main Menu.' 
                % (withdraw_val, tag_value))
            self.return_to_main(event="<Buttton-1>")
        else: # No entry given
            pass


    ###############################################################
    # ACTIVATE RETURN HOME BUTTON
    ###############################################################
    def return_to_main(self, event):
        ''' Returns to Main Frame. '''

        self.curr_balance_text.config(state="normal")
        self.curr_balance_text.delete(0, END)
        self.curr_balance_text.insert(END, '$' + format(self.curr_balance, '.2f'))
        self.curr_balance_text.config(state="disabled")  
        
        # Clear current contents
        for widget in (self.user_date, self.user_amount, 
            self.year_filter, self.month_filter,
            self.hist_year_filter, self.hist_month_filter):
            widget.delete(0, END)
        
        # Erase previous rows of Show Summary Frame
        self.erase_previous_rows(offset=0)
        
        # Reset global vars
        global user_year
        global user_month
        user_year, user_month = (0, 0) 
    
        self.main_frame.tkraise()
        return


# Run ExpensesTracker GUI
root = Tk()
root.title('Financial Visualizer')
root.geometry("580x580")
my_tracker = ExpenseTracker(master=root)
root.mainloop()
