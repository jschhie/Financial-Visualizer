# Personal Expenses Tracker GUI
> Created in Summer (August) 2020. Written in Python.

## Project Overview
An interactive GUI that helps track, categorize, and visualize all transactions (i.e., withdrawals/deposits).

## Table of Contents
* [Features](https://github.com/jschhie/expenseTracker/#features)
* [Program Requirements](https://github.com/jschhie/expenseTracker/#program-requirements)
* [Visual Demo](https://github.com/jschhie/expenseTracker/#visual-demo)
  * [Remark on Sample Resources](https://github.com/jschhie/expenseTracker/#sample-resources-in-detail)
  * [Examples](https://github.com/jschhie/expenseTracker/#examples)
* [Acknowledgments](https://github.com/jschhie/expenseTracker/#acknowledgments)

## Features
- GUI and visual graphs are supported by the ```tkinter``` and ```matplotlib``` modules
- Database stores transaction records and retrieves relevant records through ```sqlite3``` queries
  - Avoids SQL injection and exceptions at runtime by ensuring that all user input is valid
- Allows users to cancel a transcation and return to the Main Menu at any time
- Total balance reflects the changes made during all of the user's sessions

## Program Requirements
This Python program simply requires the user to install ```matplotlib``` (and ```python```!). They can the run the program as-is.

## Visual Demo
The following results are based on the supplied ```curr_balance.pickle``` file and ```expenses.db``` database. 

To better understand the outputs, please read the [next section](https://github.com/jschhie/expenseTracker/#sample-resources-in-detail). Or, skip ahead for the  [examples](https://github.com/jschhie/expenseTracker/#examples).

### Sample Resources in Detail
#### Table I: Snippet of Records 
| TID | Month | Day | Year | Amount | Is_Withdrawal | Tag |
| :---: | :---: | :---: | :---:| :---: | :---: | :---:|
| 1 | 1 | 1 | 2002 | 1.11 | 0 | None |
| 2 | 1 | 15 | 2002 | 12.99 | 1 | 'Food/Drink' |
| 3 | 1	| 31 | 2002	| 31.00 | 1	| 'Bills' | 
| ... | ...	| ... | ...	| ... | ...	| ... | 

Table I is a snippet of the ```sample_records.csv``` (See the /updated_demos/ directory for the full list of records).

Each record represents a successful transaction and is identified by a Transaction ID, or *TID*. 

In particular, the *Is_Withdrawal* field stores a boolean, which indicates if the *amount* was deposited or withdrawn on the specified date. The last field, *Tag*, pertains to money withdrawals only. By default, the latter two fields will be set to False/None for all deposits, respectively.

The current implementation has six available tags as follows: 'Shopping', 'Health', 'Bills', 'Travel', 'Food/Drink', and 'Other'. 

Lastly, *Month* is a digit, *k* that correponds to the *k*th calendar month. For example, if *k*=12, the respective record was committed on the 12th month--namely, December.

### Examples
| User Request | Program Output | Notes |
| :---: | :---: | :---: |
| None | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/main-menu.png" width="350" height="350"> | (Initial Program State) |
| New Transaction | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/make_new_txn_page.png" width="350" height="350"> | Choose to deposit/withdraw amount |
| Deposit | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/successful_deposit.png" width="300" height="180"> | Program will notify user of successful deposit/withdrawal | 
| Continue with Withdrawal | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/choose_tag.png" width="350" height="350"> | Associate transaction with a Tag |
| View History | <img src="https://github.com/jschhie/expenseTracker/blob/master/updated_demos/view_history_page.png" width="350" height="350"> | Choose viewing mode |

## Acknowledgments
This was an independent project. While writing the source code, I relied on various online tutorials, documentations, and examples. All visual demos and sample resources (such as the database instance) were also created by myself. 

Through this project, I learned about and applied the modules above for the first time. 

This README is in progress!
