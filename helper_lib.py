# Helper Functions to support ExpenseTracker
import matplotlib.pyplot as plt
import numpy as np

from tkinter import messagebox

palette = ['#a1b0d2', '#f2a47d', '#8ac9b5', '#fadf5e', '#bcdb76', '#e2a3cc']

digit_month_map = {1: "Jan.", 2: "Feb.", 3: "Mar.",
                    4: "Apr.", 5: "May", 6: "Jun.",
                    7: "Jul.", 8: "Aug.", 9: "Sep.",
                    10: "Oct.", 11: "Nov.", 12: "Dec."}



def check_view_filters(in_year, in_month=None, ignore_month=False):
    ''' Ensures that user input for Month and Year fields are valid.'''
    try:
        in_year = int(in_year)
        assert(in_year >= 2000 and in_year <= 2020)
        # Check if 'View By Year Only' Button selected
        if (ignore_month == False):
            # Attempt to convert Month Entry field into integer
            in_month = int(in_month)
            assert(in_month >= 1 and in_month <= 12)
            # Success
            return (in_year, in_month)
        else:
            # Success, but ignore month field
            return (in_year, -1)
    except:
        add_str = "" 
        if (ignore_month == False):
            add_str = " and month"
        messagebox.showerror("Input Error", 
            "Please provide valid year%s." % add_str)
        return () # Failure



def check_txn_input(pending_total, pending_change, user_date, is_deposit_txn):
    ''' Checks for valid amount to deposit/withdraw and valid
    date entry in (MM/DD/YYYY) format. '''
    try:
        pending_change = float(pending_change)
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
            month, day, year = user_date.split('/')
            for date_input in (month, day, year):
                assert(date_input.isnumeric())

            assert(int(month) <= 12 and int(month) > 0)
            assert(int(day) <= 31 and int(month) > 0)
            assert(int(year) >= 2000 and int(year) <= 2020)

            if (enough_funds == False):
                messagebox.showwarning('Insufficient Funds',
                    'Amount to withdraw is greater than current balance.')
            # Successful New Transaction (Deposit/Withdraw)
            return (pending_total, month, day, year, pending_change)
        except:
            messagebox.showerror("Input Error",
                "Please use (MM/DD/YYYY) format.\
                \nYear should be between 2000 and 2020.")
    except:
        messagebox.showerror("Input Error", "Please enter a valid, positive amount.")
    return () # Empty tuple



def show_plot(exp_values, exp_labels, u_month, u_year):
    '''Displays transactions for selected timeframe, categorized by tags or txn type (deposits/expenses)'''
    fig, ax = plt.subplots(figsize=(10,5))
    miny = min(exp_values)
    ax.set(ylim = (miny - 500 if miny < 0 else 0, max(exp_values)  + 500))
    
    bars = plt.bar(exp_labels, exp_values, color=palette, width=0.4, align='center', bottom=None)
    plt.title('Transactions Summary for %s %d' % (digit_month_map[u_month], u_year), fontweight='bold')
    plt.xlabel("Category", size=12)
    plt.ylabel("Total ($) expenses", size=12)
    ax.bar_label(bars, padding=10, fmt='${:.0f}')

    plt.show()



def show_year_chart(total_deposits, total_withdrawals, user_year):
    '''Displays year-based summary, organized by transaction type (deposits/expenses)'''
    labels = list(digit_month_map.values())
    height = 0.30
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8,8))
    xmin = min(total_deposits + total_withdrawals) # in case negative values
    ax.set(xlim = (xmin - 500 if xmin < 0 else 0, max(total_deposits + total_withdrawals) + 500))
    rects1 = ax.barh(y - height, total_deposits, height, label='Total Deposits', color=palette[0])
    rects2 = ax.barh(y, total_withdrawals, height, label='Total Expenses', color=palette[1])

    ax.set_xlabel('Total Transactions ($) Amount')
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    ax.legend(loc='upper right', frameon=False, markerscale=2)

    ax.bar_label(rects1, padding=10, fmt='${:.0f}')
    ax.bar_label(rects2, padding=10, fmt='${:.0f}')

    plt.xlabel('Total Transactions ($) Amount')
    plt.ylabel('Months')
    plt.title('Summary for ' + str(user_year), fontweight='bold')
    plt.show()
