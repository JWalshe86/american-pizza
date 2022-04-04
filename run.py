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
        #raise error if user enters a number of values different than the number required
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
    # for 1 to 5 values inserted by the user, raise error if there is any value that can not be
    # converted into int or if any value can't be found in the list provided                 
    if(len(values) > 1):
        for value in values:   
            try:
                int(value)
            except ValueError:
                print("\n" + colored("Invalid data: ", "red") + "Wrong numbers format, please try again.\n")
                return False
            try:   
                if value.upper() not in list_to_check:
                    raise ValueError(
                        "We didn't recognised your value"
                    )
            except ValueError as e:
                print("\n" + colored("Invalid data: ", "red") + f"{e}, please try again.\n")
                return False   
    # for exactly one value inserted by te user, raise error if value can't be found in the
    # list provided                 
    else:                 
        try:   
            if values[0].upper() not in list_to_check:
                raise ValueError(
                    "We didn't recognised your value"
                )
        except ValueError as e:
            print("\n" + colored("Invalid data: ", "red") + f"{e}, please try again.\n")
            return False    

    return True
    

def display_pizza_menu(orders_list):
    """
    Displays a welcome message and the pizza menu for the user.
    A variable will memorise the user's input value representing 
    the pizza's code for the order
    """  
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "Welcome to " + colored('American pizza', 'green') + 
          " !" + "\033[0m \n") 
    print("Here is our" + "\033[1m" + " pizza menu " + "\033[0m" + 
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
        print("Please enter the code for your pizza choice"
              " by choosing a number between 1 and 6"+ "\n" + "OR" )
        print("\033[1m"+"(P) " + "\033[0m" + "to see what your order contains until this moment\n")
        print("* You can only pick one pizza type at a time with the option to"
              " add to your order later\n")

        pizza_type = input("\033[1m" + "Write your answer here: \n" + "\033[0m" )

        user_data = pizza_type.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "P"], 1):
            if user_data[0].upper() == "P":
                if len(orders_list) == 0:
                    print(colored("You haven't added nothing to your order yet\n\n", "yellow"))
                    time.sleep(1)
                    continue
                else:    
                    print("Your order contains:") 
                    for order in orders_list:
                        print(colored(order.get_string(), "yellow"))
                        print("\n\n")
                        time.sleep(1)
                    continue 

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
    size for the pizza.
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
        print("Please enter the code for your pizza size choice (S, M, L)" + "\n" + "OR" )
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to pizza sizes and prices guide\n")

        pizza_size = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = pizza_size.split(" ")

        if validate_data(user_data, ["S", "M", "L", "B"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "B":
                print("We get you back to pizza menu...")
                time.sleep(2)
            else:
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def get_custom_pizza_sauce():
    """
    Displays a sugestive message for user and the sauces catalogue as the 
    first step in creating a custom pizza.
    A variable will memorise the user's input value representing the chosen
    sauce for the custom pizza.
    """ 
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "This is the first step in creating your custom pizza." + 
          "\nPlease choose an option for your sauce." + "\033[0m \n") 

    sauces = SHEET.worksheet("sauces")
    data = sauces.get_all_values()

    # define header names
    col_names = data[0]

    # define sizes catalogue data
    sauces_data = data[-3:]

    print(tabulate(sauces_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    while True:      
        print("Enter a number between 1 and 3" + "\n" + "OR")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_sauce = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = custom_pizza_sauce.split(" ")

        if validate_data(user_data, ["1", "2", "3", "R"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(2)
            else:
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def get_custom_pizza_cheese():
    """
    Displays a sugestive message for user and the options for cheese
    in a table as the second step in creating a custom pizza.
    A variable will memorise the user's input value representing the chosen
    cheese option for the custom pizza.
    """ 
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "This is the second step in creating your custom pizza." + 
          "\nPlease choose an option for the cheese." + "\033[0m \n") 

    cheese = SHEET.worksheet("cheese")
    data = cheese.get_all_values()

    # define header names
    col_names = data[0]

    # define sizes catalogue data
    cheese_data = data[-2:]

    print(tabulate(cheese_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    while True:      
        print("Choose between the options 1 and 2" + "\n" + "OR")
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to sauces options")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_cheese = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = custom_pizza_cheese.split(" ")

        if validate_data(user_data, ["1", "2", "B", "R"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "B":
                print("We get you back to sauces options...")
                time.sleep(2)
            elif user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(2)
            else:  
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def get_custom_pizza_topings():
    """
    Displays a sugestive message for user and the options for topings
    in a table as the last step in creating a custom pizza.
    A variable will memorise the user's input value representing the chosen
    topings for the custom pizza.
    """ 
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "This is the last step in creating your custom pizza." + 
          "\nYou can choose up to 5 topings for your pizza" + "\033[0m \n") 

    topings = SHEET.worksheet("topings")
    data = topings.get_all_values()

    # define header names
    col_names = data[0]

    # define sizes catalogue data
    topings_data = data[-10:]

    print(tabulate(topings_data, headers=col_names, tablefmt="fancy_grid") + 
          "\n\n")
    while True:      
        print("Enter numbers between 1 and 10 separated by spaces, not more than five." + "\n" + "OR")
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to cheese options")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_topings = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = custom_pizza_topings.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "B", "R"], 5):
            print("\n\nData is valid!")
            if user_data[0].upper() == "B":
                print("We get you back to cheese options...")
                time.sleep(2)
            elif user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(2)
            else:  
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data  


def get_pizza_quantity():
    """
    Displays a sugestive message for user.
    A variable will memorise the user's input value representing the chosen
    quantity for the pizza.
    """  
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "Please insert the quantity that you want, not more than 10" + "\033[0m \n") 

    while True:      
        print("Enter a number between 1 and 10" + "\n" + "OR" )
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        pizza_quantity = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = pizza_quantity.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "R"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "B":
                print("We get you back to pizza sizes and prices guide...")
                time.sleep(2)
            elif user_data[0].upper() == "R":
                print("We get you to back to pizza menu...")
                time.sleep(2)
            else:
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def get_values_for_custom_pizza():
    values = []
    custom_pizza_sauce = get_custom_pizza_sauce() 
    if custom_pizza_sauce.upper() == "R":
        values.append("restart")
        return values  
    else:
        values.append(custom_pizza_sauce.upper())    
    custom_pizza_cheese = get_custom_pizza_cheese()
    while custom_pizza_cheese.upper() == "B":
        custom_pizza_sauce = get_custom_pizza_sauce()
        custom_pizza_cheese = get_custom_pizza_cheese()
    if custom_pizza_cheese.upper() == "R":
        values.append("restart") 
        return values
    else:
        values.append(custom_pizza_cheese.upper())    
    custom_pizza_topings = get_custom_pizza_topings()
    while custom_pizza_topings[0].upper() == "B":
        custom_pizza_cheese = get_custom_pizza_cheese()
        while custom_pizza_cheese.upper() == "B":
            custom_pizza_sauce = get_custom_pizza_sauce()
            custom_pizza_cheese = get_custom_pizza_cheese()
        custom_pizza_topings = get_custom_pizza_topings()
    if custom_pizza_topings[0].upper() == "R":
        values.append("restart") 
        return values
    else:
        values.append(custom_pizza_topings)     
    return values    


def finalize_order(orders_list):
    """
    Displays a sugestive message for user.
    A variable will memorise the user's input value representing the option for 
    adding or not elements to the order.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "You're almost ready!" + "\033[0m \n") 
    print("Your order contains:") 
    for order in orders_list:
        print(colored(order.get_string(), "yellow"))
    print("\n") 

    while True:      
        print("Do you want to add something else?" + "\033[1m" + "(Y/N)" + "\033[1m" )

        answer = input("\033[1m" + "Write your answer here: \n" + "\033[1m" )

        user_data = answer.split(" ")

        if validate_data(user_data, ["Y", "N"], 1):
            print("\n\nData is valid!")
            if user_data[0].upper() == "Y":
                print("We get you back to pizza menu")
                time.sleep(2)
            else:
                print("We get you to the next step...")
                time.sleep(2)
            break

    return user_data[0]  


def get_sheet_values(type, size, custom_values):

    pizzas = SHEET.worksheet("pizzas")
    sizes = SHEET.worksheet("sizes")
    sauces = SHEET.worksheet("sauces")
    cheese = SHEET.worksheet("cheese")
    topings = SHEET.worksheet("topings")

    pizzas_data = pizzas.get_all_values()
    sizes_data = sizes.get_all_values()
    sauces_data = sauces.get_all_values()
    cheese_data = cheese.get_all_values()
    topings_data = topings.get_all_values()

    pizza_type_string = " "
    for row in pizzas_data[-6:]:
        if row[0] == type:
            pizza_type_string = row[1]

    pizza_size_string = " "
    for row in sizes_data[-3:]:
        if row[0] == size.upper():
            pizza_size_string = row[1]   

    pizza_sauce_string = " "
    pizza_cheese_string = " "
    pizza_topings_strings = []
    if custom_values != " ":
        for row in sauces_data[-3:]:
            if row[0] == custom_values[0]:
                pizza_sauce_string = row[1]

        for row in cheese_data[-2:]:
            if row[0] == custom_values[1]:
                pizza_cheese_string = row[1]   

        for row in topings_data[-10:]:
            for toping in custom_values[2]:
                if row[0] == toping:
                    pizza_topings_strings.append(row[1])   
    else:
        pizza_sauce_string = " "
        pizza_cheese_string = " "
        pizza_topings_strings = " "

    return pizza_type_string, pizza_size_string, pizza_sauce_string, pizza_cheese_string, pizza_topings_strings


def main():
    """
    Run all program functions
    """  
    class PizzaOrder:
        def __init__(self, type, size, sauce, cheese, topings, quantity):
            self.type = type
            self.size = size
            self.sauce = sauce
            self.cheese = cheese
            self.topings = topings             
            self.quantity = quantity

        def get_string(self):
            if self.sauce == " ":
                # generate string for custom pizza
                pizza_string = f"{self.quantity} X {self.size} {self.type} "
                if int(self.quantity) > 1:
                    pizza_string += "pizzas"
                else:
                     pizza_string += "pizza" 

                return  pizza_string

            else:
                # generate string for normal pizza
                custom_pizza_string = f"{self.quantity} X {self.size} Custom "
                if int(self.quantity) > 1:
                    custom_pizza_string += "pizzas "
                else:
                    custom_pizza_string += "pizza " 

                custom_pizza_string += f"({self.sauce}, {self.cheese}, "   

                for ind in range(len(self.topings)):
                    custom_pizza_string += self.topings[ind]

                    if ind != len(self.topings) - 1:
                        custom_pizza_string += ", " 
                    else:
                        custom_pizza_string += ")"

                return custom_pizza_string

    add_to_order = False

    # create loops so the user have the possibility to return to the previous steps
    # when user's input = "B" and restart the order when user's input = "R"
    while True:
        if add_to_order == False:
            orders_list = []
        pizza_type = display_pizza_menu(orders_list)
        pizza_size = display_pizza_sizes()
        while pizza_size.upper() == "B":
            pizza_type = display_pizza_menu(orders_list)
            pizza_size = display_pizza_sizes()

        if pizza_type == "6":
            custom_pizza_values = get_values_for_custom_pizza()
            if custom_pizza_values[len(custom_pizza_values)-1] == "restart":
                continue   
        else:
            custom_pizza_values = " "        
        pizza_quantity = get_pizza_quantity()
        if pizza_quantity.upper() == "R":
            continue  

        sheet_values = get_sheet_values(pizza_type, pizza_size, custom_pizza_values)   
        type = sheet_values[0] 
        size = sheet_values[1]
        sauce = sheet_values[2]
        cheese = sheet_values[3]
        topings = sheet_values[4]

        order = PizzaOrder(type, size, sauce, cheese, topings, pizza_quantity)
        orders_list.append(order)

        finalize_order_value = finalize_order(orders_list)  
        if finalize_order_value.upper() == "Y":
            add_to_order = True
            continue  
 
        for order in orders_list:
            print(order.get_string())

        break  
  


main()