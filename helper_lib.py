# Helper Functions to support ExpenseTracker
import matplotlib.pyplot as plt
import numpy as np

from tkinter import messagebox



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
    ''' Creates and displays Pie Chart.'''
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



def autolabel(rects):
    ''' Sub-helper function to autolabel each bar in the multi-bar graph. ''' 
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.0 * height,
        '%d' % int(height),
        ha='center', va='bottom')



def show_bar_chart(total_deposits, total_withdrawals, user_year):
    # Creates and displays the Grouped Bar Chart.
    bar_width = 0.25
    r1 = np.arange(len(total_deposits))
    r2 = [x + bar_width for x in r1]

    rects1 = plt.bar(r1, total_deposits, width=bar_width, 
        edgecolor='white', label='Total Deposits')
    
    rects2 = plt.bar(r2, total_withdrawals, width=bar_width, 
        edgecolor='white', label='Total Withdrawals')

    plt.xlabel('Month')
    plt.ylabel('Transactions Amount ($)')
    plt.title('Expenses Report for %d: Transactions Grouped by Month' % user_year)
    plt.xticks([r + bar_width for r in range(len(total_deposits))], 
        list((digit_month_map).values()))

    autolabel(rects1)
    autolabel(rects2)

    plt.legend()
    plt.show()