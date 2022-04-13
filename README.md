# Personal Finance Tracker GUI

## Project Overview
A Tkinter graphical user interface (GUI) in Python that helps track, categorize, and visualize all personal transactions (i.e., withdrawals/deposits).

From creating this project, I learned about some of Python's many libraries at once and integrated them into a single GUI application. 

## Table of Contents
* [Current Features](https://github.com/jschhie/expenseTracker/#current-features)
* [Program Requirements](https://github.com/jschhie/expenseTracker/#program-requirements)
* [Visual Demo](https://github.com/jschhie/expenseTracker/#visual-demo)

## Current Features
- GUI functionality and data visualization are supported by ```tkinter```, ```matplotlib```, and ```numpy```.
- Database stores transaction records and retrieves relevant records through ```sqlite3``` queries.
- Total balance reflects the changes made during all of the user's sessions.
- Available tags to categorize transactions: 'Shopping', 'Health', 'Bills', 'Travel', 'Food/Drink', and 'Other'.

## Program Requirements
This Python program simply requires the user to install ```matplotlib``` (and ```python3```!). 

To run the program on Terminal, for example, enter ``` python3 finance_tracker.py ```.

<details><summary><b>Show Details</b></summary>

As-is, the program has been initialized with some sample transactions, which are stored in the database ```expenses.db``` and ```curr_balance.pickle``` file. Alternatively, the user may provide their own input and "reset" the program's state. To do so, they need not download those two aforementioned files. The ```ExpenseTracker``` would then be emptied with a balance of $0.00.

</details>


## Visual Demo
The following results are based on the supplied ```curr_balance.pickle``` file and ```expenses.db``` database. 


### Table II: Sample User Requests & Program Responses
| User Request | Program Response | Key Notes |
| :---: | :---: | :---: |
| [0] ```None``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/new_main_menu.png"> | (Initial Program State) |
| [1] ```New Transaction``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/new_txn_page.png"> | Choose to deposit/withdraw amount |
| [1.A] ```Deposit``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/successful_deposit.png"> | Program will notify user of successful deposit/withdrawal | 
| [1.B] ```Continue with Withdrawal``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/choose_tag_page.png"> | Associate transaction with a Tag |
| [2] ```Visualize Transactions``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/new_view_history_page.png"> | Choose viewing mode |
| [2.A] ```View deposits vs. withdrawals```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/sample_all_txns.png" width="350" height="350"> | In this case, view report for January 2002 |  
| [2.B] ```View by Tags```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/sample_by_tags.png" width="350" height="350"> | In this case, view report for January 2002, by tags | 
| [2.C] ```View by Year Only```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/new_bar_chart.png" width="350" height="350"> | Here, view report for Year=2002 as a whole (Group by Transaction Type and Month) |
| [3] ``` View History ``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/summary_input.png" width="380" height="250"> | Get details on records for January 2002 |
| [3.A] ``` Show Expenses Summary ``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/valid_txns/show_more_records.png" width="350" height="350">| Display details for first 10 records for January 2002. User can optionally see next 10 records by clicking the 'Show More Records' button. | 

