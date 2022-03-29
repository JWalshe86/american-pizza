import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('american_pizza_order_system')


def display_pizza_menu():
    """
    Displays a welcome message and the pizza menu for the user.
    A variable will memorise the user's input value representing 
    the pizza's code for the order
    """  
    print("\033[1m" + "Welcome to " + colored('American pizza', 'green') + 
          " !" + "\033[0m \n") 
    print("Here is our" + "\033[1m" + " pizza menu " + "\033[1m" + 
          "for today:\n\n")

    pizzas = SHEET.worksheet("pizzas")
    data = pizzas.get_all_values()

    # define header names
    col_names = data[0]

    # define menu content and set width for Ingredients column
    menu_data = data[-6:]
    for row in menu_data:
        if(len(row[2]) > 45):
            last_space_index = row[2][:45].rfind(" ")
            row[2] = row[2][:last_space_index + 1] + "\n" + row[2][last_space_index + 1:]

    # print(menu_data)        

    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    print("To start the order please enter the code for your pizza choice"
          " (1, 2, 3, 4, 5, 6)\n")
    print("* You can only pick one pizza type at a time with the option to add"
          " to your order later\n")


def main():
    """
    Run all program functions
    """  
    display_pizza_menu()


main()