# visual.py: This script creates visualizations of financial data using seaborn and matplotlib.
# It provides insights into spending habits by category and over time.


import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import calendar


# Logging setup
logging.basicConfig(filename='budget_manager/logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function for getting date period.
def get_user_input_month():
    """
    This function does the following:
    1. Prompts the user to input a year and a month.
    2. Validates the user's input for the month (1-12).
    3. Constructs a start date and end date for the specified month.
    4. Returns the start date, end date, and the full month name.

    Returns:
    - start_date (str): The first day of the specified month in "yyyy-mm-dd" format.
    - end_date (str): The last day of the specified month in "yyyy-mm-dd" format.
    - month_name (str): The full name of the specified month.
    """


    while True:
        year = int(input("Enter the year (yyyy): "))
        month = int(input("Enter the month (1-12): "))
        
        if 1 <= month <= 12:
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]}"
            month = calendar.month_name[month]
            return start_date, end_date, month
        else:
            print("Invalid month. Please enter a valid month (1-12).")

# Here we define planned expenditures by category (edit it if you added your own categories).
planned_expenditure = pd.DataFrame({
    'category': ['food', 'entertainment', 'transport', 'home', 'other'],
    'planned': [285, 100, 25, 75, 100]
})


# Function to choose the color for one-bar-graph.
def get_single_color(percent):
    """
    This function determines a color based on a given percentage value.

    Args:
    - percent (float): A percentage value between 0 and 1.

    Returns:
    - color (str): A color name based on the input percentage.

    Color Choices:
    - 'skyblue' for percent < 0.35
    - 'limegreen' for 0.35 <= percent < 0.6
    - 'orange' for 0.6 <= percent < 0.8
    - 'red' for percent >= 0.8
    """

    if percent < 0.35:
        return 'skyblue'
    elif percent < 0.6:
        return 'limegreen'
    elif percent < 0.8:
        return 'orange'
    return 'red'

# Function to get a pallet for multiple-bar-graph.
def get_color_pallete(dataframe):
    """
    This function generates a color palette based on percentage values in a DataFrame.

    Args:
    - dataframe (pandas.DataFrame): A DataFrame containing a 'percent' column with values between 0 and 1.

    Returns:
    - palette (list): A list of color names corresponding to the 'percent' values in the DataFrame.

    The function iterates through the rows of the DataFrame and uses the 'get_single_color' function to determine a color for each 'percent' value.
    It then returns a list of color names representing the palette.
    """

    pallete = []
    
    for _, row in  dataframe.iterrows():
        pallete.append(get_single_color(row['percent']))


    return pallete


# Plotting function.
def plotting():
    """
    This function takes time period and creates plots.

    The function performs the following steps:
    1. Obtains a time period (start_date, end_date, and month) using the 'get_user_input_month' function.
    2. Connects to the database to fetch spending data.
    3. Computes daily spending, category spending, and summary of all expenses.
    4. Creates three subplots 
    5. Saves them to the .png file
    """
    
    # Getting time period.
    try:
        start_date, end_date, month = get_user_input_month()
    except:
        logging.error("Invalid input date format.")
        raise TypeError("Invalid input date format.")

    
    # Connect to the database
    conn = sqlite3.connect('budget_manager/data.db')

    # Take the sum of expenses for grouped by day.
    query = f"""
    SELECT date, SUM(spent) AS total_spent
    FROM budget
    WHERE date BETWEEN '{start_date}' AND '{end_date}' AND category != 'na'
    GROUP BY date
    ORDER BY date
    """
    daily_spending = pd.read_sql_query(query, conn)
    daily_spending['planned'] = sum(planned_expenditure['planned']) / 30
    daily_spending['percent'] = daily_spending['total_spent'] / daily_spending['planned']

    # Take the sum of expenses for each category.
    query2 = f"""
    SELECT category, SUM(spent) AS total_spent
    FROM budget
    WHERE date BETWEEN '{start_date}' AND '{end_date}' AND category != 'na'
    GROUP BY category
    """
    category_spending = pd.read_sql_query(query2, conn)\
        .merge(planned_expenditure, on='category', how='right')\
        .fillna(0)\
        .sort_values(by='planned', ascending=False)
    category_spending['percent'] = category_spending['total_spent'] / category_spending['planned']

    # Close the database connection.
    conn.close()

    # Summary of all expenses.
    sum_expenses = pd.DataFrame({
        'month': [month],
        'spent': [category_spending['total_spent'].sum()],
        'planned': [planned_expenditure['planned'].sum()],
        'percent': [category_spending['total_spent'].sum() / planned_expenditure['planned'].sum()],
        'all': [725]
        })
    

    # Create a figure with two subplots.
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Plot 1: Plot for daily spendings.
    ax[0] = sns.barplot(data=daily_spending, x='date', y='planned', ax=ax[0], label='Planned', color='lightyellow', edgecolor='black', hatch='///')
    ax[0] = sns.barplot(data=daily_spending, x='date', y='total_spent', ax=ax[0], palette=get_color_pallete(daily_spending), edgecolor='black')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Total Spending')
    ax[0].set_title(f'Daily Spendings in {month}')
    ax[0].tick_params(axis='x', rotation=45)
    ax[0].legend(loc='upper right', bbox_to_anchor=(1.1, 1))

    # Plot 2: Plot for categories.
    ax[1] = sns.barplot(data=category_spending, x='category', y='planned', ax=ax[1], label='Planned Expenditure', color='lightyellow', edgecolor='black', hatch='///')
    ax[1] = sns.barplot(data=category_spending, x='category', y='total_spent', ax=ax[1], label='Actual Spending', palette=get_color_pallete(category_spending), edgecolor='black')
    ax[1].set_xlabel('Category')
    ax[1].set_ylabel('Total Spending')
    ax[1].set_title(f'Spendings by Categories in {month}')
    ax[1].tick_params(axis='x', rotation=45)
    ax[1].set_xticklabels(category_spending['category'])
    ax[1].legend(loc='upper right', bbox_to_anchor=(1.2, 1))

    # Plot 3: month budget plot.
    ax[2] = sns.barplot(data=sum_expenses, x='month', y='all', ax=ax[2], label='Savings', color='white', edgecolor='black', hatch='')
    ax[2] = sns.barplot(data=sum_expenses, x='month', y='planned', ax=ax[2], label='Planned', color='lightyellow', edgecolor='black', hatch='///')
    ax[2] = sns.barplot(data=sum_expenses, x='month', y='spent', ax=ax[2], label='Spent', edgecolor='black', color=get_single_color(sum_expenses['percent'].sum()))
    ax[2].set_xlabel(f"Total spent: {round(sum_expenses['spent'].sum(), 2)}")
    ax[2].set_ylabel('Value')
    ax[2].set_title(f'All Spendings in Selected Period')
    ax[2].legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    ax[2].set_yticks([0, 100, 220, 350, 460, 580, 725])

    # Adjust layout.
    plt.tight_layout()


    # Save the plot to a file.    
    plt.savefig('budget_manager/graph.png')

    # Show the plot.
    plt.show()


if __name__ == "__main__":
    plotting()
