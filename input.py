# input.py: This script imports financial transaction data from an Excel file into the SQLite database.
# It processes the data and handles data insertion.


import pandas as pd
import sqlite3
import logging

# Setting up logging to capture the data import process and any errors.
logging.basicConfig(filename='budget_manager/logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read and process an Excel file.
def read_excel_file(file_path):
    try:
        # Read the Excel file into a DataFrame with specified header and skipfooter.
        # Adjust these parameters according to the format of your Excel file.
        return pd.read_excel(file_path, header=12, skipfooter=7)
    except FileNotFoundError:
        logging.error("File not found.")
        raise

# Function to insert records from DataFrame into SQLite database.
def insert_records(conn, input_file):
    cursor = conn.cursor()
    # Iterate through each row of the DataFrame.
    for _, row in input_file.iterrows():
        # Extract and format the data from each row.
        date, spent, received, operation = row['date'], row['spent'], row['received'], row['operation']
        transaction_type = 'income' if received else 'outcome'
        
        try:
            # Insert data into the database.
            cursor.execute('INSERT OR IGNORE INTO budget (date, transaction_type, spent, received, operation) VALUES (?, ?, ?, ?, ?)',
                           (date, transaction_type, spent, received, operation))
        except sqlite3.IntegrityError as e:
            # Log a warning if the record already exists.
            logging.warning(f"Record for {date} already exists. Skipped.")

# Main function to process the input file and insert data.
def main():
    # Path to the Excel file.
    input_file_path = 'budget_manager/bank_statement_example.xls'

    # Connecting to the SQLite database.
    conn = sqlite3.connect('budget_manager/data.db')
    try:
        # Read the Excel file and preprocess the data.
        input_file = read_excel_file(input_file_path)
        # Additional data preprocessing steps can be added here.
        
        # Insert the processed data into the database.
        insert_records(conn, input_file)
        conn.commit()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        conn.rollback()
    finally:
        # Close the database connection.
        conn.close()

if __name__ == "__main__":
    main()
