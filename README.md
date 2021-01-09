# Personal Finance Tracker GUI
> Created in Summer 2020 as an independent project. Written in Python.

## Project Overview
A graphical user interface (GUI) that helps track, categorize, and visualize all personal transactions (i.e., withdrawals/deposits).

While writing the source code, I relied on various online tutorials and code documentations. From creating this project, I learned about some of Python's many libraries at once and integrated them into a single GUI application. 

## Table of Contents
* [Current Features](https://github.com/jschhie/expenseTracker/#current-features)
* [Program Requirements](https://github.com/jschhie/expenseTracker/#program-requirements)
* [About the Sample Resources](https://github.com/jschhie/expenseTracker/#about-the-sample-resources)
* [Visual Demo](https://github.com/jschhie/expenseTracker/#visual-demo)

## Current Features
- GUI functionality and data visualization are supported by ```tkinter```, ```matplotlib```, and ```numpy```.
- Database stores transaction records and retrieves relevant records through ```sqlite3``` queries
  - Avoids SQL injection and exceptions at runtime by ensuring that all user input is valid
- Allows users to cancel a transaction and return to the Main Menu at any time
- Total balance reflects the changes made during all of the user's sessions

## Program Requirements
This Python program simply requires the user to install ```matplotlib``` (and ```python3```!). 

To run the program on Terminal, for example, enter ``` python3 finance_tracker.py ```.

<details><summary><b>Show Details</b></summary>

As-is, the program has been initialized with some sample transactions, which are stored in the database ```expenses.db``` and ```curr_balance.pickle``` file. Alternatively, the user may provide their own input and "reset" the program's state. To do so, they need not download those two aforementioned files. The ```ExpenseTracker``` would then be emptied with a balance of $0.00.

</details>

## About the Sample Resources
### Table I: Snippet of DB Records
| TID | Month | Day | Year | Amount | Is_Withdrawal | Tag |
| :---: | :---: | :---: | :---:| :---: | :---: | :---:|
| 1 | 1 | 1 | 2002 | 1.11 | 0 | None |
| 2 | 1 | 15 | 2002 | 12.99 | 1 | 'Food/Drink' |
| 3 | 1	| 31 | 2002	| 31.00 | 1	| 'Bills' | 
| ... | ...	| ... | ...	| ... | ...	| ... | 


<details><summary><b>Show Table I Details</b></summary>

Table I is a snippet of the ```sample_records.csv```. See the [updated_demos](https://github.com/jschhie/expenseTracker/tree/master/updated_demos) for the full list of records.

Each record represents a successful transaction and is identified by a Transaction ID, or *TID*. 

In particular, the *Is_Withdrawal* field stores a boolean, which indicates if the *Amount* was deposited or withdrawn on the specified date. The last field, *Tag*, pertains to money withdrawals only. By default, the last two fields will be set to False/None for all deposits, respectively.

The current implementation has six available tags as follows: 'Shopping', 'Health', 'Bills', 'Travel', 'Food/Drink', and 'Other'. 

Lastly, *Month* is a digit, *k* that correponds to the *k*th calendar month. For example, if *k*=12, the respective record was committed on the 12th month--namely, December.

</details>

## Visual Demo
The following results are based on the supplied ```curr_balance.pickle``` file and ```expenses.db``` database. 

To better understand the outputs, please read the section [above](https://github.com/jschhie/expenseTracker/#about-the-sample-resources).

### Table II: Sample User Requests & Program Responses
| User Request | Program Response | Key Notes |
| :---: | :---: | :---: |
| [0] ```None``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/new_main_menu.png"> | (Initial Program State) |
| [1] ```New Transaction``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/new_txn_page.png"> | Choose to deposit/withdraw amount |
| [1.A] ```Deposit``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/successful_deposit.png"> | Program will notify user of successful deposit/withdrawal | 
| [1.B] ```Continue with Withdrawal``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/choose_tag_page.png"> | Associate transaction with a Tag |
| [2] ```Visualize Transactions``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/new_view_history_page.png"> | Choose viewing mode |
| [2.A] ```View deposits vs. withdrawals```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/sample_all_txns.png" width="350" height="350"> | In this case, view report for January 2002 |  
| [2.B] ```View by Tags```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/sample_by_tags.png" width="350" height="350"> | In this case, view report for January 2002, by tags | 
| [2.C] ```View by Year Only```| <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/new_bar_chart.png" width="350" height="350"> | Here, view report for Year=2002 as a whole (Group by Transaction Type and Month) |
| [3] ``` View History ``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/summary_input.png" width="380" height="250"> | Get details on records for January 2002 |
| [3.A] ``` Show Expenses Summary ``` | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/summary_table.png" width="350" height="350">| Display details for first 10 records for January 2002 | 

<details><summary><b>Show Table II Details</b></summary>

Again, Table II's entries reflect the sample data provided; it does not show the *entire* process of committing/inputting all of the transactions into the database. Table II also does not show the program's response to all possible user input errors. If interested, please see the [updated_demos](https://github.com/jschhie/expenseTracker/tree/master/updated_demos) for all the generated error messages.

</details>
