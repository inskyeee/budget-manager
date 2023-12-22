# Budget Manager

A Python-based budget management tool to categorize and visualize financial transactions. This project uses SQLite for database management and seaborn/matplotlib for data visualization.

## Project Structure

```plaintext
budget_manager/
├── bank_statement_example.xls    # Example bank statement in Excel format
├── categorization.py             # Script for categorizing transactions
├── data.db                       # SQLite database for storing transaction data
├── graph.png                     # Output visualization of the budget data
├── input.py                      # Script for reading and inserting data into the database
├── logger.log                    # Log file for tracking application logs
└── visual.py                     # Script for visualizing budget data
```


### categorization.py

Script for automatically categorizing financial transactions based on predefined keywords and user input. It uses SQLite for database operations and includes logging for tracking categorization activities.

### input.py

A utility script to read transaction data from an Excel file and insert it into the SQLite database. It handles data formatting and error logging.

### visual.py

Generates visual representations of financial data using seaborn and matplotlib. It provides insights into spending patterns by category and time.

## Installation and Usage

1. Clone the repository to your local machine.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Run `input.py` to load your financial data into the database.
4. Execute `categorization.py` to categorize your transactions.
5. Use `visual.py` to generate visual insights into your spending.

## Features

- **Automated Categorization**: Automatically categorize transactions based on predefined keywords. Allows manual categorization for unclassified transactions.
- **Data Import**: Easily import transaction data from Excel files into a SQLite database for processing and analysis.
- **Interactive Visualizations**: Generate insightful visualizations of spending patterns, including categorization and time-based spending trends, using seaborn and matplotlib.
- **Customizable Categories**: Flexibility to define and modify transaction categories and associated keywords.
- **Transaction Logging**: Comprehensive logging system to track the process of transaction categorization and errors.
- **User Input for Categorization**: Interactive user prompts to categorize transactions that cannot be auto-categorized.
 
## Contributing

Contributions to enhance the functionality or efficiency of the Budget Manager are welcome. Feel free to fork the repository and submit pull requests.

## License

This project is open-sourced under the MIT License.
