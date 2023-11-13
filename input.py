import pandas as pd
import sqlite3
import logging

#Logging setup
logging.basicConfig(filename='budget_manager/logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#File reading function
def read_excel_file(file_path):
    try:
        #You need to customize this setting for your file type
        return pd.read_excel(file_path, header=12, skipfooter=7) #header=where your transaction table starts; skipfooter=how many rows to skip in the end
    except FileNotFoundError:
        logging.error("File not found.")
        raise

#Function for inserting data in database
def insert_records(conn, input_file):
    
    cursor = conn.cursor()
    
    #Here we insert data from each row to the database
    for _, row in input_file.iterrows():
        date = row['date'].strftime('%Y-%m-%d')
        spent = row['spent']
        received = row['received']
        operation = row['operation']
        transaction_type = 'income' if not spent else 'outcome'

        try:
            cursor.execute('INSERT OR IGNORE INTO budget (date, transaction_type, spent, received, operation) VALUES (?, ?, ?, ?, ?)',
                           (date, transaction_type, spent, received, operation))
        except sqlite3.IntegrityError:
            logging.warning(f"Record for {date} already exists. Skipped.")


#Main body of the program
def main():
    #Defining the input file (choose your own path)
    input_file_path = 'budget_manager/bank_statement_example.xls'

    #Connecting to the database file
    conn = sqlite3.connect('budget_manager/data.db')

    #Trying to apply all changes needed for the bank statement (works only with a certain type of bank statements)
    try:
        input_file = read_excel_file(input_file_path)
        input_file = input_file.rename(columns={'Date': 'date',
                                                'Recipient/Payer': 'recipient_payer',
                                                'Outcome': 'spent',
                                                'Income': 'received',
                                                'Operation': 'operation'})
        
        input_file['date'] = pd.to_datetime(input_file['date'], format='%d.%m.%Y')
        input_file['spent'] = input_file['spent'].str.replace(',', '.').astype(float)
        input_file['received'] = input_file['received'].str.replace(',', '.').astype(float)

        insert_records(conn, input_file)
        conn.commit()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        #Here we close the connection
        conn.close()
    


#Running the program
if __name__ == "__main__":
    main()
