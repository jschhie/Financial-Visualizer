# Personal Expenses Tracker GUI
> Created in August 2020. Written in Python.

## Project Overview
An interactive GUI that helps track, categorize, and visualize all transactions (i.e., withdrawals/deposits).

## Features
- GUI and visual graphs are supported by the ```tkinter``` and ```matplotlib``` modules
- Database stores transaction records and retrieves relevant records through ```sqlite3``` queries
  - Avoids SQL injection and exceptions at runtime by ensuring that all user input is valid
- Allows users to cancel a transcation and return to the Main Menu at any time

## Requirements
This Python program simply requires the user to install ```matplotlib``` (and ```python```!). They can the run the program as-is.

## Visual Demo
The following results are based on the supplied ```curr_balance.pickle``` file and ```expenses.db``` database. 

To better understand the outputs, please read the section below. 

#### Table I: Snippet of Records 
| TID | Month | Day | Year | Amount | Is_Withdraw | Tag |
| :---: | :---: | :---: | :---:| :---: | :---: | :---:|
| 1 | 1 | 1 | 2002 | 1.11 | 0 | None |
| 2 | 1 | 15 | 2002 | 12.99 | 1 | 'Food/Drink' |
| 3 | 1	| 31 | 2002	| 31.00 | 1	| 'Bills' | 
| ... | ...	| ... | ...	| ... | ...	| ... | 

Table I is a snippet of the ```sample_records.csv``` (See the /updated_demos/ directory for the full list of records).

Each record represents a successful transaction and is identified by a Transaction ID, or *TID*. 

In particular, the *Is_Withdraw* field stores a boolean, which indicates if the *amount* was deposited or withdrawn on the specified date. The last field, *Tag*, pertains to money withdrawals only. By default, the latter two fields will be set to False/None for all deposits, respectively.

> Notes: 
> The current implementation has six available tags as follows: 'Shopping', 'Health', 'Bills', 'Travel', 'Food/Drink', and 'Other'. 
> Lastly, *Month* is a digit, in which *k* correponds to the *k*th calendar month.

# TODO: Add demos here

## Acknowledgments
This was an independent project. All visual demos and sample resources (such as the database instance) were also created by myself. While writing the source code, I relied on various online tutorials, documentations, and examples. Through this project, I learned about and applied the modules above for the first time. 

This README is in progress!
