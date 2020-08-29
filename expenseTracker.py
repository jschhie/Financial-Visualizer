# Personal Expenses Tracker GUI
from tkinter import *
from tkinter import messagebox

import sqlite3 as sqlite
import pickle
import matplotlib.pyplot as plt

conn = sqlite.connect('expenses.db')

digit_month_map = {1: "Jan.", 2: "Feb.", 3: "Mar.", 
                    4: "Apr.", 5: "May", 6: "Jun.", 
                    7: "Jul.", 8: "Aug.", 9: "Sep.",
                    10: "Oct.", 11: "Nov.", 12: "Dec."}

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
        
        # Create/Load SQL Database
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
        # Save current session's transactions and updated balance
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
            text="Please specify year and month.").grid(column=1)
        
        # Add Filter Modes (Year and Month)
        Label(self.history_frame, text="Year (YYYY): ").grid(row=1, sticky=E)
        Label(self.history_frame, text="Month (MM): ").grid(row=2, sticky=E)

        self.year_filter = Entry(self.history_frame)
        self.year_filter.grid(row=1, column=1)
        self.month_filter = Entry(self.history_frame)
        self.month_filter.grid(row=2, column=1)

        # TODO: Validate user input from above
        # Assuming valid for now

        view_tags_button = Button(self.history_frame, text="View By Tags")
        view_tags_button.bind("<Button-1>", self.view_by_tag)
        view_tags_button.grid(row=3, column=1)

        view_all_button = Button(self.history_frame, 
            text="View Deposits vs. Withdrawals")
        view_all_button.bind("<Button-1>", self.view_all)
        view_all_button.grid(row=4, column=1)

        # Back to Main Menu Button
        back_button = Button(self.history_frame, text="Return to Main Menu")
        back_button.bind("<Button-1>", self.return_to_main)
        back_button.grid(row=5, column=1)


    def check_view_filters(self):
        try:
            in_year = int(self.year_filter.get())
            in_month = int(self.month_filter.get())
            assert(in_year >= 2000 and in_year <= 2020)
            assert(in_month >= 1 and in_month <= 12)
            return (in_year, in_month) # Success
        except:
            messagebox.showerror("Input Error", 
                "Please provide valid month and year combination.")
            return () # Failure


    def show_plot(self, exp_values, exp_labels, u_month, u_year):
        # Set up pie chart
        fig, ax = plt.subplots()
        ax.pie(exp_values, labels=exp_labels, autopct='%1.1f%%', pctdistance=0.85)
        ax.axis('equal')

        # Draw Donut within Pie
        center_circle = plt.Circle((0,0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        # Plot data
        plt.title('Expenses Report for %s %d' % (digit_month_map[u_month], u_year))
        plt.tight_layout()
        plt.show()


    def view_by_tag(self, event):
        ''' Perform SQL Query to view Transactions by Tag for specified year and month. '''
        # Check for valid numeric inputs
        if (len(filters:=self.check_view_filters()) == 0):
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

        self.show_plot(exp_values=all_amounts, 
            exp_labels=all_tags,
            u_month=user_month, u_year=user_year)


    def view_all(self, event):
        ''' Perform SQL Query to view all withdrawals versus deposits during 
        specified month and year. '''
        if (len(filters:=self.check_view_filters()) == 0):
            return

        # Otherwise, unpack filters
        user_year, user_month = filters

        # debugging, changed sum to count()
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

        self.show_plot(exp_values=[deposits, withdrawals], 
            exp_labels=['Deposits', 'Withdrawals'],
            u_month=user_month, u_year=user_year)


    def check_txn_input(self, is_deposit_txn):
        ''' Checks for valid amount to deposit/withdraw and valid 
        date entry in (MM/DD/YYYY) format. '''
        # Check User Amount first
        try:
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
            # Next, check User Dates
            try:
                user_date = self.user_date.get()
                month, day, year = user_date.split('/')
                for date_input in (month, day, year):
                    assert(date_input.isnumeric())

                assert(int(month) <= 12 and int(month) > 0)
                assert(int(day) <= 31 and int(month) > 0)
                assert(int(year) >= 2000 and int(year) <= 2020)

                # Warn user if any insufficient funds but continue to process txn
                if (enough_funds == False):
                    messagebox.showwarning('Insufficient Funds', 
                        'Amount to withdraw is greater than current balance.')
                # Successful New Transaction (Deposit/Withdraw)
                self.curr_balance = pending_total
                # Return a tuple of user input
                return (month, day, year, pending_change)
            except:
                # Indicate txn failure
                messagebox.showerror("Input Error", 
                    "Please use (MM/DD/YYYY) format.\
                    \nYear should be between 2000 and 2020.")
        except:
            # Indicate txn failure
            messagebox.showerror("Input Error", "Please enter a valid, positive amount.")
        return () # Empty tuple

    
    def add_new_txn(self, event):
        self.new_txn_frame.tkraise()


    def deposit_money(self, event):
        self.results_tuple = self.check_txn_input(is_deposit_txn=True)
        if len(self.results_tuple) > 0:
            # Insert new deposit entry into database
            conn.execute(''' INSERT INTO EXPENSES 
                (MONTH, DAY, YEAR, AMOUNT) \
                VALUES (?, ?, ?, ?)''', self.results_tuple)
            # Indicate successful deposit
            deposit_val = format(self.results_tuple[3], '.2f')
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
        self.results_tuple = self.check_txn_input(is_deposit_txn=False)
        if len(self.results_tuple) > 0:
            # Valid input received as results
            self.withdraw_frame.tkraise()
        else:
            # results_tuple is empty tuple meaning invalid user input
            # Remain on current Frame
            pass


    def get_tag(self, event):
        widget = event.widget
        if (selections:=widget.curselection()):
            # Get corresponding Tag
            idx = int(selections[0])
            tag_value = widget.get(idx)
            # Insert new record as withdrawal
            month, day, year, amount = self.results_tuple
            conn.execute(''' INSERT INTO EXPENSES 
               (MONTH, DAY, YEAR, AMOUNT, IS_WITHDRAW, TAG) \
               VALUES (?, ?, ?, ?, 1, ?)''', (month, day, year, amount, tag_value))
            # Indicate successful withdrawal
            withdraw_val = format(amount, '.2f')
            messagebox.showinfo('Successful Transaction',
                'Withdrawal of $%s for %s completed.\nReturning to Main Menu.' 
                % (withdraw_val, tag_value))
            # Redirect to Main Menu
            self.return_to_main(event="<Buttton-1>")
            

    def view_history(self, event):
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
        for widget in (self.user_date, self.user_amount, self.year_filter, self.month_filter):
            widget.delete(0, END)
        # Redirect to Main Frame
        self.main_frame.tkraise()


# Run ExpensesTracker GUI
root = Tk()
root.geometry("500x500")
root.title('Personal Expenses Tracker')
my_tracker = ExpenseTracker(master=root)
root.mainloop()
