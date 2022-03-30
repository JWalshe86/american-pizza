import gspread
import time
import os
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


def validate_data(values, list_to_check, number_of_values_required):
    """
    This function checks if the values provided by the user in the values 
    parameter meet the requirements about the number_of_values_required.
    Also checks if their format is correct and can be found in list_to_check
    provided by the user when the function is called.
    If any of the requirements is not respected it throws an error to inform
    the user.  
    """
    try:
        if number_of_values_required == 1:
            if(len(values) > 1):
                raise ValueError(
                    f"Exactly 1 value required, you provided {len(values)}"
                )
        else:
            if(len(values) > 5):
                raise ValueError(
                    "You can not choose more than 5 topings"
                )
    except ValueError as e:
        print("\n" + colored("Invalid data: ", "red") + f"{e}, please try again.\n")
        return False
    try:
        for value in values:
            if value.upper() not in list_to_check:
                raise ValueError(
                    "We didn't recognised your values"
                )
    except ValueError as e:
        print("\n" + colored("Invalid data: ", "red") + f"{e}, please try again.\n")
        return False    

    return True
    

def display_pizza_menu():
    """
    Displays a welcome message and the pizza menu for the user.
    A variable will memorise the user's input value representing 
    the pizza's code for the order
    """  
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

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

    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    while True:      
        print("To start the order please enter the code for your pizza choice"
              " by choosing a number between 1 - 6\n")
        print("* You can only pick one pizza type at a time with the option to"
              " add to your order later\n")

        pizza_type = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = pizza_type.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6"], 1):
            print("\n\nData is valid!")
            print("We get you to the next step...")
            time.sleep(2)
            break

    return user_data[0]        


def display_pizza_sizes():
    """
    Displays a sugestive message for user and the pizza catalogue for sizes and 
    prices.
    A variable will memorise the user's input value representing the chosen
    size for the pizza or 
    """  
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "Here is our catalogue for sizes and prices."
          " Wich one do you preffer?" + "\033[0m \n") 

    sizes = SHEET.worksheet("sizes")
    data = sizes.get_all_values()

    # define header names
    col_names = []
    for ind in range(1, 5):
        column = sizes.col_values(ind)
        col_names.append(column[0])

    # define sizes catalogue data
    sizes_data = data[-3:]

    print(tabulate(sizes_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    while True:      
        print("Please enter the code for your pizza size choice (S, M, L)" + "\n" +
              "\033[1m" + "OR" + "\033[1m")
        print("(B) to go back to our pizza menu\n")

        pizza_size = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = pizza_size.split(" ")

        if validate_data(user_data, ["S", "M", "L", "B"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "B":
                print("We get you back to pizza menu")
                time.sleep(2)
            else:
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def main():
    """
    Run all program functions
    """  
    pizza_type = display_pizza_menu()
    pizza_size = display_pizza_sizes()
    while pizza_size.upper() == "B":
        pizza_type = display_pizza_menu()
        pizza_size = display_pizza_sizes()
    print(pizza_type)    
    print(pizza_size)


main()