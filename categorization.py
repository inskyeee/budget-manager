# categorization.py: This script is responsible for categorizing financial transactions based on predefined
# categories and keywords. It automates the categorization process and allows manual categorization.


import sqlite3
import logging

# Configure logging to capture important messages and errors.
logging.basicConfig(filename='budget_manager/logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Predefined categories and keywords for auto-categorization.
categories = {'f': 'food', 'e': 'entertainment', 't': 'transport', 'h': 'home', 'o': 'other', 'n': 'na'}
keywords = {'food': ['starbucks', 'waitrose', 'cupp', 'sainsburys', 'morrison', 'tesco', 'iceland', 'cafe', 'coffee', 'lidl'], 
            'transport': ['first', 'uber'], 
            'home': ['circuit', 'ikea'], 
            'other': ['three']}

# Function to automatically categorize expenses based on keywords.
def auto_categorize(cursor, rowid, operation):
    # Iterate through each category and its associated keywords.
    for category, category_keywords in keywords.items():
        for keyword in category_keywords:
            if keyword in operation.lower():
                # Update the category in the database if a keyword is found in the transaction description.
                cursor.execute('UPDATE budget SET category=? WHERE rowid=?', (category, rowid))
                logging.info(f"Auto-categorized rowid {rowid} as {category}")
                return True
    return False

# Main function to categorize expenses.
def categorize_expenses():
    # Connect to the SQLite database.
    conn = sqlite3.connect('budget_manager/data.db')
    cursor = conn.cursor()

    # Begin a transaction to categorize each expense.
    try:
        conn.execute('BEGIN')
        cursor.execute('SELECT rowid, date, spent, operation FROM budget WHERE category="NaN"')
        for row in cursor.fetchall():
            rowid, date, spent, operation = row
            # Attempt to auto-categorize the transaction.
            auto_categorized = auto_categorize(cursor, rowid, operation)

            # If auto-categorization fails, prompt the user for manual categorization.
            if not auto_categorized:
                print(f"Date: {date}\n\nValue: {spent} £\n\nDescription:\n{operation}\n\n")
                user_input = input("Enter category (food, entertainment, transport, home, other, na): ").strip().lower()

                # Map user input to the corresponding category and update the database.
                try:
                    category = categories[user_input[0]]
                    cursor.execute('UPDATE budget SET category=? WHERE rowid=?', (category, rowid))
                    logging.info(f"Category updated for rowid {rowid}: {category}")

                    # Commit the transaction.
                    conn.commit()
                except KeyError:
                    logging.error(f"Invalid category entered for rowid {rowid}: {user_input}")
                    print("Invalid category entered.")
            else:
                # Commit the transaction for auto-categorized entries.
                conn.commit()
    except Exception as e:
        # Rollback the transaction in case of any error.
        conn.rollback()
        logging.error(f"An error occurred: {str(e)}")
    finally:
        # Close the database connection.
        conn.close()

if __name__ == '__main__':
    categorize_expenses()
