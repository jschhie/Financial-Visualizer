# Personal Expenses Tracker GUI
> Created in August 2020. Written in Python.

## Project Overview
An interactive GUI that helps track and visualize all transactions (i.e., withdrawals/deposits).

## Features
- GUI and visual graphs are supported by Tkinter and matlibplot modules, respectively
- Database stores transaction records and retrieves relevant records through SQLite3 queries
  - Avoids SQL injection and exceptions at runtime by ensuring that all user input is valid
- Allows users to cancel a transcation and return to the Main Menu at any time

## Visual Demo
The following results are based on the supplied ```curr_balance.pickle``` file and ```expenses.db``` database. 

In the table below, each record represents a successful transaction and is identified by a Transaction ID, or *TID*. In particular, the *Is_Withdraw* field stores a boolean, which indicates if the *amount* was deposited or withdrawn on the specified date. The last field, *Tag*, pertains to money withdrawals only. By default, the latter two fields will be set to False/None for all deposits.

> Note: The current implementation has six available tags as follows: 'Shopping', 'Health', 'Bills', 'Travel', 'Food/Drink', and 'Other'.



## Acknowledgments
This was an independent project. All visual demos and sample resources (such as the database instance) were also created by myself. While writing the source code, I relied on various online tutorials, documentations, and examples. Through this project, I learned about and applied the modules above for the first time. 

Lastly, this README is in progress!
