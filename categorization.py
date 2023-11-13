import sqlite3
import logging

#Logging setup
logging.basicConfig(filename='budget_manager/logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Dictionary of categories
categories = {'f': 'food', 'e': 'entertainment', 't': 'transport', 'h': 'home', 'o': 'other', 'n': 'na'}

#You can put your own keywoards for each category
keywords = {'food': ['starbucks', 'waitrose', 'cupp', 'sainsburys', 'morrison', 'tesco', 'iceland', 'cafe', 'coffee', 'lidl'], 'transport': ['first', 'uber'], 'home': ['circuit', 'ikea'], 'other': ['three']}

#Function to automatically categorize expenses based on keywords
def auto_categorize(cursor, rowid, operation):
    for category, category_keywords in keywords.items():
        for keyword in category_keywords:
            if keyword in operation.lower():
                cursor.execute('UPDATE budget SET category=? WHERE rowid=?', (category, rowid))
                logging.info(f"Auto-categorized rowid {rowid} as {category}")
                return True
    return False



#Function to categorize expenses
def categorize_expenses():
    #Connecting to the database
    conn = sqlite3.connect('budget_manager/data.db')
    cursor = conn.cursor()
    
    try:
        #Start a transaction
        conn.execute('BEGIN')

        #Fetch rows where category is "NaN"
        cursor.execute('SELECT rowid, date, spent, operation FROM budget WHERE category="NaN"')

        for row in cursor.fetchall():
            rowid, date, spent, operation = row

            #Check for auto-categorization based on keywords
            auto_categorized = auto_categorize(cursor, rowid, operation)


            if not auto_categorized:
                print(f"Date: {date}\n\nValue: {spent} £\n\nDescription:\n{operation}\n\n")
                user_input = input("Enter category (food, entertainment, transport, home, other, na): ").strip().lower()
                print('\n------------------------------------------------------------\n')

                try:
                    category = categories[user_input[0]]
                    cursor.execute('UPDATE budget SET category=? WHERE rowid=?', (category, rowid))
                    logging.info(f"Category updated for rowid {rowid}: {category}")

                    #Commit the transaction
                    conn.commit()
                except:
                    logging.error(f"Invalid category entered for rowid {rowid}: {user_input}")
                    raise NameError
            else:
                #Commit the transaction
                conn.commit()
    except Exception as e:
        #Rollback the transaction in case of any error
        conn.rollback()
        logging.error(f"An error occurred: {str(e)}")
    finally:
        #Close the database connection
        conn.close()

if __name__ == '__main__':
    categorize_expenses()
