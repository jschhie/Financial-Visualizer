''' Initializes all ExpenseTracker frames '''
from tkinter import *



def init_main(root):        
    ''' Initialize Main Frame. '''
    Label(root.main_frame, text="Financial Visualizer", font=('Arial', 20, 'bold')).grid(column=1, padx=20, pady=20)
    Label(root.main_frame, text="Current Balance: ", font=('Arial', 15, 'bold'), padx=20).grid(sticky=E)

    root.curr_balance_text = Entry(root.main_frame)
    root.curr_balance_text.insert(END, '$' + format(root.curr_balance, '.2f'))
    root.curr_balance_text.config(state="disabled")
    root.curr_balance_text.grid(row=1, column=1, padx=20, pady=20)
    
    Label(root.main_frame, text="Choose an Action: ", font=('Arial', 15, 'bold'), padx=20).grid(row=2, sticky=E)

    new_txn_button = Button(root.main_frame, text="New Transaction", width=20)
    new_txn_button.bind("<Button-1>", root.add_new_txn)
    new_txn_button.grid(row=2, column=1, padx=5, pady=5)

    visualize_button = Button(root.main_frame, text="Visualize Data", width=20)
    visualize_button.bind("<Button-1>", root.visualize_txn)
    visualize_button.grid(row=3, column=1, padx=5, pady=5)        
    
    view_button = Button(root.main_frame, text="View History", width=20)
    view_button.bind("<Button-1>", root.view_history)
    view_button.grid(row=4, column=1, padx=5, pady=5)

    quit_button = Button(root.main_frame, text="Save", width=20)
    quit_button.bind("<Button-1>", root.custom_quit)
    quit_button.grid(row=5, column=1, padx=5, pady=5)



def init_new_txn(root):
    ''' Initialize New Transaction Frame. '''
    Label(root.new_txn_frame, text="Add New Transaction", font=('Arial', 20, 'bold')).grid(column=1, padx=20, pady=20)

    Label(root.new_txn_frame, text="Amount: ", font=('Arial', 15, 'bold'), padx=20).grid(row=1, sticky=E)
    root.user_amount = Entry(root.new_txn_frame)
    root.user_amount.grid(row=1, column=1, padx=5, pady=5)

    Label(root.new_txn_frame, text="Date (MM/DD/YYYY): ", font=('Arial', 15, 'bold'), padx=20).grid(row=2, sticky=E)
    root.user_date = Entry(root.new_txn_frame)
    root.user_date.grid(row=2, column=1, padx=20, pady=20)

    deposit_button = Button(root.new_txn_frame, text="Deposit", width=20)
    deposit_button.bind("<Button-1>", root.deposit_money)
    deposit_button.grid(row=3, column=1, padx=5, pady=5)

    withdraw_button = Button(root.new_txn_frame, text="Withdraw", width=20)
    withdraw_button.bind("<Button-1>", root.withdraw_money)
    withdraw_button.grid(row=4, column=1, padx=5, pady=5)

    back_button = Button(root.new_txn_frame, text="Return Home", width=20)
    back_button.bind("<Button-1>", root.return_to_main)
    back_button.grid(row=5, column=1, padx=5, pady=5)



def init_withdraw(root):
    ''' Initialize New Frame specifically for Withdrawals. '''
    Label(root.withdraw_frame, text="Continue to Withdrawl.", font=('Arial', 15, 'italic')).grid(column=1, padx=15, pady=15)
    Label(root.withdraw_frame, text="Available Tags: ", font=('Arial', 15, 'bold')).grid(row=1, sticky=E, padx=20)

    tags_listbox = Listbox(root.withdraw_frame, selectmode=BROWSE, height=7)
    tags = ['Shopping', 'Health', 'Food/Drink', 'Bills', 
        'Travel', 'Entertainment', 'Other']
    
    for tag in tags:
        tags_listbox.insert(END, tag)
    
    tags_listbox.bind("<<ListboxSelect>>", root.get_tag)
    tags_listbox.grid(row=1, column=1, padx=20, pady=20)

    back_button = Button(root.withdraw_frame, text="Return Home", width=20)
    back_button.bind("<Button-1>", root.return_to_main)
    back_button.grid(row=5, column=1, padx=5, pady=5)



def init_visualize(root):
    ''' Initialize Visualize Transactions Frame. '''
    Label(root.visualize_frame, text="Please specify year (and month).", font=('Arial', 15, 'italic'), padx=20).grid(columnspan=2, padx=20, pady=20)        
    Label(root.visualize_frame, text="Year (YYYY): ", font=('Arial', 15, 'bold'), padx=20).grid(row=1, sticky=E)
    Label(root.visualize_frame, text="Month (MM): ", font=('Arial', 15, 'bold'), padx=20).grid(row=2, sticky=E)

    root.year_filter = Entry(root.visualize_frame)
    root.year_filter.grid(row=1, column=1, padx=5, pady=5)
    root.month_filter = Entry(root.visualize_frame)
    root.month_filter.grid(row=2, column=1, padx=20, pady=20)

    Label(root.visualize_frame, text="View By: ", font=('Arial', 15, 'bold'), padx=20).grid(row=3, sticky=E)

    view_tags_button = Button(root.visualize_frame, text="Tags", width=20)
    view_tags_button.bind("<Button-1>", root.view_by_tag)
    view_tags_button.grid(row=3, column=1, padx=5, pady=5)

    view_all_button = Button(root.visualize_frame, 
        text="Deposits vs. Withdrawals", width=20)
    view_all_button.bind("<Button-1>", root.view_all)
    view_all_button.grid(row=4, column=1, padx=5, pady=5)

    view_by_year_button = Button(root.visualize_frame, text="Year Only", width=20)
    view_by_year_button.bind("<Button-1>", root.view_by_year)
    view_by_year_button.grid(row=5, column=1, padx=5, pady=5)

    back_button = Button(root.visualize_frame, text="Return Home", width=20)
    back_button.bind("<Button-1>", root.return_to_main)
    back_button.grid(row=6, column=1, padx=5, pady=5)



def init_history(root):
    ''' Initialize View History Frame. '''
    # Add filter modes (year and month)
    Label(root.history_frame, 
    text="Please specify year and month. ", font=('Arial', 15, 'italic')).grid(columnspan=2, padx=20, pady=20)
    Label(root.history_frame, text="Year (YYYY): ", font=('Arial', 15, 'bold'), padx=20).grid(row=1, sticky=E)
    Label(root.history_frame, text="Month (MM): ", font=('Arial', 15, 'bold'), padx=20).grid(row=2, sticky=E)

    root.hist_year_filter = Entry(root.history_frame)
    root.hist_year_filter.grid(row=1, column=1, padx=5, pady=5)
    root.hist_month_filter = Entry(root.history_frame)
    root.hist_month_filter.grid(row=2, column=1, padx=20, pady=20)

    show_summary_button = Button(root.history_frame, text="Show Expenses Summary", width=20)
    show_summary_button.bind("<Button-1>", root.show_summary)
    show_summary_button.grid(row=3, column=1, padx=5, pady=5)

    back_button = Button(root.history_frame, text="Return Home", width=20)
    back_button.bind("<Button-1>", root.return_to_main)
    back_button.grid(row=4, column=1, padx=5, pady=5)



def init_summary(root):
    ''' Initialize Summary Frame. '''
    header_a = "Displaying 10 transactions at a time."
    header_b = "Click 'Show More' to see additional records."

    prompt_a = Label(root.summary_frame, text=header_a, font=('Arial', 15, 'italic'), pady=20).grid(row=0, columnspan=3)
    prompt_b = Label(root.summary_frame, text=header_b, font=('Arial', 15, 'italic'), pady=10).grid(row=1, columnspan=3)

    header_amt = Label(root.summary_frame, text="Amount", font=('Arial', 15, 'bold')).grid(row=2, sticky=W, padx=5, pady=5)
    header_date = Label(root.summary_frame, text="Date", font=('Arial', 15, 'bold')).grid(row=2, column=1, sticky=W, padx=5, pady=5)
    header_tag = Label(root.summary_frame, text="Tag", font=('Arial', 15, 'bold')).grid(row=2, column=2, sticky=W, padx=5, pady=5)

    # Show More Button (in case > 10 records retrieved)
    show_more_button = Button(root.summary_frame, text="Show More", width=20)
    show_more_button.bind("<Button-1>", root.show_more_records)
    show_more_button.grid(row=13, column=1, padx=20, pady=20)

    back_button = Button(root.summary_frame, text="Return Home", width=20)
    back_button.bind("<Button-1>", root.return_to_main)
    back_button.grid(row=14, column=1, padx=10, pady=5)        