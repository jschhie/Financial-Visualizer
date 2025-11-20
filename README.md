# Financial Visualizer
> Python, Tkinter, Matplotlib, SQLite.

## Project Overview
A Tkinter-based graphical user interface (GUI) application for tracking, categorizing, and visualizing personal expenses and deposits.

---

## Table of Contents
* [Visual Demos](https://github.com/jschhie/expenseTracker/#visual-demos)
* [Program Requirements](https://github.com/jschhie/expenseTracker/#program-requirements)

---

## Visual Demos

| Home View | Show Expenses Summary |
|:---: | :---: |
|<img src="https://github.com/jschhie/Financial-Visualizer/blob/master/updated_demos/home3.png" width="450"> |<img src="https://github.com/jschhie/Financial-Visualizer/blob/master/updated_demos/summary3.png" width="450">|

| View by Tags | View by Year Only |
| :---:| :---: |
|<img src="https://github.com/jschhie/Financial-Visualizer/blob/master/updated_demos/by%20month%20year%20tag.png" width="450">| <img src="https://github.com/jschhie/Financial-Visualizer/blob/master/updated_demos/double%20barh.png" width="450"> |

| View deposits vs. withdrawals |
|:---: |
| <img src="https://github.com/jschhie/Financial-Visualizer/blob/master/updated_demos/by%20dep%20exp.png" width="450"> |


---

## Program Requirements

This GUI requires ```matplotlib``` and ```numpy```. To install these dependencies, run the following commands:

1. Clone this repository:
```bash
git clone https://github.com/jschhie/Financial-Visualizer.git [folderNameHere]
```

2. Navigate into the folder:
```bash
cd [folderNameHere]
```

3. Create and activate virtual environment (`venv`):
> To isolate the project's dependencies
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required packages:
```bash
pip3 install -r requirements.txt
```

5. To start the GUI app, run: 
```bash
python3 finance_tracker.py
```
