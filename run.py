from datetime import date, datetime, timedelta
import time
import os
import random
import pytz
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
        # raise error if user enters a number of values
        # different than the number required
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
    except ValueError as error:
        print("\n" + colored("Invalid data: ", "red") + f"{error}, please try"
              " again.\n")
        return False
    # for 1 to 5 values inserted by the user, raise error if there is any
    # value that can not be converted into int or if any value can't be found
    # in the list provided
    if(len(values) > 1):
        for value in values:
            try:
                int(value)
            except ValueError:
                print("\n" + colored("Invalid data: ", "red") +
                      "Wrong numbers format, please try again.\n")
                return False
            try:
                if value.upper() not in list_to_check:
                    raise ValueError(
                        "We didn't recognised your value"
                    )
            except ValueError as error:
                print("\n" + colored("Invalid data: ", "red") + f"{error}, "
                      "please try again.\n")
                return False
    # for exactly one value inserted by te user, raise error if value can't be
    # found in the list provided
    else:
        try:
            if values[0].upper() not in list_to_check:
                raise ValueError(
                    "We didn't recognised your value"
                )
        except ValueError as error:
            print(
                "\n" + colored("Invalid data: ", "red") + f"{error}, "
                "please try again.\n"
                )
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
            row[2] = row[2][:last_space_index + 1] + "\n" \
                + row[2][last_space_index + 1:]

    # print pizza menu table
    print(tabulate(menu_data, headers=col_names, tablefmt="fancy_grid") +
          "\n\n")
    while True:
        print("Please enter the code for your pizza choice"
              " by choosing a number between 1 and 6" + "\n" + "OR")
        print("\033[1m"+"(P) " + "\033[0m" + "to see what your order contains "
              "until this moment\n")
        print("* You can only pick one pizza type at a time with the option to"
              " add to your order later\n")

        pizza_type = input("\033[1m" + "Write your answer here: \n" +
                           "\033[0m")

        # creates a list with every value inserted by the user
        user_data = pizza_type.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "P"], 1):
            if user_data[0].upper() == "P":
                if len(orders_list) == 0:
                    print(colored("You haven't added nothing to your order yet"
                                  "\n\n", "yellow"))
                    time.sleep(1)
                    continue
                else:
                    print("Your order contains:")
                    for order in orders_list:
                        print(colored(order.get_string(), "yellow"))
                        print("\n\n")
                        time.sleep(1)
                    continue

            print("We get you to the next step...")
            time.sleep(1)
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

    # define header names
    col_names = []
    for ind in range(1, 5):
        column = sizes.col_values(ind)
        col_names.append(column[0])

    # define sizes catalogue data
    sizes_data = []
    for ind in range(2, 5):
        row = sizes.row_values(ind)
        sizes_data.append(row[:4])

    print(tabulate(sizes_data, headers=col_names, tablefmt="fancy_grid") +
          "\n\n")
    while True:
        print("Please enter the code for your pizza size choice (S, M, L)" +
              "\n" + "OR")
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to pizza sizes and" +
              " prices guide\n")

        pizza_size = input("\033[1m" + "Write your answer here: \n" +
                           "\033[1m")

        # creates a list with every value inserted by the user
        user_data = pizza_size.split(" ")

        if validate_data(user_data, ["S", "M", "L", "B"], 1):
            if user_data[0].upper() == "B":
                print("We get you back to pizza menu...")
                time.sleep(1)
            else:
                print("We get you to the next step...")
                time.sleep(1)
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

    # print sauces table
    print(tabulate(sauces_data, headers=col_names, tablefmt="fancy_grid") +
          "\n\n")
    while True:
        print("Enter a number between 1 and 3" + "\n" + "OR")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_sauce = input("\033[1m" + "Write your answer here: \n" +
                                   "\033[1m")

        # creates a list with every value inserted by the user
        user_data = custom_pizza_sauce.split(" ")

        if validate_data(user_data, ["1", "2", "3", "R"], 1):
            if user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(1)
            else:
                print("We get you to the next step...")
                time.sleep(1)
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

    print("\033[1m" + "This is the second step in creating your " +
          "custom pizza.\nPlease choose an option for the cheese." +
          "\033[0m \n")

    cheese = SHEET.worksheet("cheese")
    data = cheese.get_all_values()

    # define header names
    col_names = data[0]

    # define sizes catalogue data
    cheese_data = data[-2:]

    # print cheese table
    print(tabulate(cheese_data, headers=col_names, tablefmt="fancy_grid") +
          "\n\n")
    while True:
        print("Choose between the options 1 and 2" + "\n" + "OR")
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to sauces options")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_cheese = input("\033[1m" + "Write your answer here: \n" +
                                    "\033[1m")

        # creates a list with every value inserted by the user
        user_data = custom_pizza_cheese.split(" ")

        if validate_data(user_data, ["1", "2", "B", "R"], 1):
            if user_data[0].upper() == "B":
                print("We get you back to sauces options...")
                time.sleep(1)
            elif user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(1)
            else:
                print("We get you to the next step...")
                time.sleep(1)
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

    # print topings table
    print(tabulate(topings_data, headers=col_names, tablefmt="fancy_grid") +
          "\n\n")
    while True:
        print("Enter numbers between 1 and 10 separated by spaces, " +
              "not more than five." + "\n" + "OR")
        print("\033[1m"+"(B) " + "\033[0m" + "to go back to cheese options")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        custom_pizza_topings = input("\033[1m" + "Write your answer here: \n" +
                                     "\033[1m")

        # creates a list with every value inserted by the user
        user_data = custom_pizza_topings.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "7", "8",
                                     "9", "10", "B", "R"], 5):
            if user_data[0].upper() == "B":
                print("We get you back to cheese options...")
                time.sleep(1)
            elif user_data[0].upper() == "R":
                print("We get you back to pizza menu...")
                time.sleep(1)
            else:
                print("We get you to the next step...")
                time.sleep(1)
            break

    return user_data


def get_pizza_quantity():
    """
    Displays a sugestive message for user.
    A variable will memorise the user's input value representing the chosen
    quantity for the pizza.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "Please insert the quantity that you want, " +
          "not more than 10" + "\033[0m \n")

    while True:
        print("Enter a number between 1 and 10" + "\n" + "OR")
        print("\033[1m"+"(R) " + "\033[0m" + "to restart your order\n")

        pizza_quantity = input("\033[1m" + "Write your answer here: \n" +
                               "\033[1m")

        # creates a list with every value inserted by the user
        user_data = pizza_quantity.split(" ")

        if validate_data(user_data, ["1", "2", "3", "4", "5", "6", "7", "8",
                                     "9", "10", "R"], 1):
            if user_data[0].upper() == "B":
                print("We get you back to pizza sizes and prices guide...")
                time.sleep(1)
            elif user_data[0].upper() == "R":
                print("We get you to back to pizza menu...")
                time.sleep(1)
            else:
                print("We get you to the next step...")
                time.sleep(1)
            break

    return user_data[0]


def get_values_for_custom_pizza():
    """
    This function is called when the user choose 'Create your own' type
    for pizza order. It calls three methods coresponding to the three
    steps for custom pizza: sauce, cheese, topings.
    These methods are called in while loops to give the user the possibility
    to get back to the previous step.
    """
    values = []
    # gets pizza sauce code
    custom_pizza_sauce = get_custom_pizza_sauce()
    if custom_pizza_sauce.upper() == "R":
        values.append("restart")
        return values
    else:
        values.append(custom_pizza_sauce.upper())

    # gets pizza cheese code
    custom_pizza_cheese = get_custom_pizza_cheese()
    while custom_pizza_cheese.upper() == "B":
        custom_pizza_sauce = get_custom_pizza_sauce()
        custom_pizza_cheese = get_custom_pizza_cheese()
    if custom_pizza_cheese.upper() == "R":
        values.append("restart")
        return values
    else:
        values.append(custom_pizza_cheese.upper())

    # gets pizza topings codes
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
    adding, finishing or restarting the order.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "You're almost ready!" + "\033[0m \n")
    print("Your order contains:")
    for order in orders_list:
        print(colored(order.get_string(), "yellow"))
    print("Total price:")
    print(colored("€ " + f"{get_total_price(orders_list)}", "green"))
    print("\n")

    while True:
        print("Please choose one of the options bellow:")
        print("\033[1m" + "(A) " + "\033[0m" + "to add to your order")
        print("\033[1m" + "(F) " + "\033[0m" + "to finish your order")
        print("\033[1m" + "(R) " + "\033[0m" + "to restart your order\n")

        answer = input("\033[1m" + "Write your answer here: \n" + "\033[1m")

        # creates a list with every value inserted by the user
        user_data = answer.split(" ")

        if validate_data(user_data, ["A", "F", "R"], 1):
            if user_data[0].upper() == "F":
                print("We process your order...")
                time.sleep(1)
            else:
                print("We get you back to pizza menu...")
                time.sleep(1)
            break

    return user_data[0]


def get_sheet_values(p_type, size, custom_values):
    """
    This function returns the string values from the sheets
    as names coresponding to codes inserted by the user
    """
    # acces every worksheet from american_pizza_order_system sheet
    pizzas = SHEET.worksheet("pizzas")
    sizes = SHEET.worksheet("sizes")
    sauces = SHEET.worksheet("sauces")
    cheese = SHEET.worksheet("cheese")
    topings = SHEET.worksheet("topings")

    # get all values from every worksheet
    pizzas_data = pizzas.get_all_values()
    sizes_data = sizes.get_all_values()
    sauces_data = sauces.get_all_values()
    cheese_data = cheese.get_all_values()
    topings_data = topings.get_all_values()

    # get pizza type name
    pizza_type_string = " "
    for row in pizzas_data[-6:]:
        if row[0] == p_type:
            pizza_type_string = row[1]

    # get pizza size name
    pizza_size_string = " "
    pizza_price = 0
    for row in sizes_data[-3:]:
        if row[0] == size.upper():
            pizza_size_string = row[1]
            pizza_price = float(row[3])
            pizza_prep_time = int(row[4])

    pizza_sauce_string = " "
    pizza_cheese_string = " "
    pizza_topings_strings = []
    # if the codes for custom pizza elements are not empty strings
    # gets coresponding codes name from sheet, else give the values an empty
    # string
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

    return pizza_type_string, pizza_size_string, pizza_sauce_string, \
        pizza_cheese_string, pizza_topings_strings, pizza_price, \
        pizza_prep_time


def get_sheet_order_refference():
    """
    Return a list with all the orders codes from the orders worksheet
    """
    orders = SHEET.worksheet("orders")
    orders_list = orders.get_all_values()

    refferences_list = []
    for row in orders_list[1:]:
        refferences_list.append(row[0])

    return refferences_list


def generate_order_refference(orders_refference):
    """
    Generate a random number between 0 and 1000 as order
    refference for user
    """
    while True:
        number = random.randint(0, 1000)
        for value in orders_refference:
            if int(value) == number:
                continue
        break

    return number


def final_menu(refference, duration):
    """
    Displays a sugestive message for user.
    A variable will memorise the user's input value representing the option for
    live orders, restart order or exit program.
    """
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\033[1m" + "Thank you!" + "\033[0m \n")
    print("Your order refference is: " + colored(refference, "green") + "\n")
    print("Estimated to be ready in: " + colored(duration, "blue") + "\n")

    while True:
        print("What do you want to do next?")
        print("\033[1m" + "(L) " + "\033[0m" + "check live orders")
        print("\033[1m" + "(R) " + "\033[0m" + "make another order")
        print("\033[1m" + "(E) " + "\033[0m" + "exit program\n")

        answer = input("\033[1m" + "Write your answer here: \n" + "\033[1m")

        # creates a list with every value inserted by the user
        user_data = answer.split(" ")

        if validate_data(user_data, ["L", "R", "E"], 1):
            if user_data[0].upper() == "L":
                print("Live Orders\n\n")
                time.sleep(1)
                continue
            elif user_data[0].upper() == "P":
                print("We get you back to pizza menu...")
                time.sleep(1)
            break

    return user_data[0]


def get_total_price(orders_list):
    """
    Calculate total price value
    """
    total = 0
    for order in orders_list:
        total += order.price
    total = round(total, 2)
    return total


def get_total_duration(orders_list):
    """
    Calculate total duration for an order
    For orders that include max 10 pizzas the duration is a sum
    between total preparation time and 15 min in the oven considering
    that the oven has a capacity of 10 pizzas
    For orders that include more than 10 pizzas the duration is a sum
    between total preparation time, 15 min in the oven and 10 min extra
    per each additional pizza
    """
    duration = 0
    quantity = 0
    # get total number of pizzas in the order
    for order in orders_list:
        quantity += int(order.quantity)

    # get total preparation time
    for order in orders_list:
        duration += order.prep_time

    # add 15 minutes for oven cooking
    duration += 15

    # add extra time if there are more than 10 pizzas
    if quantity > 10:
        extra = (quantity - 10) * 10
        duration += extra

    return duration


def get_duration_string(duration):
    """
    Return a string with the number of hours and minutes
    representing the duration of the order
    """
    if duration > 60:
        hours = int(duration / 60)
        minutes = duration - (hours * 60)
        if hours > 1:
            return f"{hours} hours and {minutes} minutes"
        else:
            return f"{hours} hour and {minutes} minutes"
    else:
        return f"{duration} minutes"


def update_orders(refference, orders_list, price, order_date, order_time,
                  duration, status):
    """
    Receive integers and strings as parameters to be inserted into orders
    worksheet
    """
    orders = SHEET.worksheet("orders")
    data = []
    data.append(refference)
    order_description = ""
    for order in orders_list:
        order_description += order.get_string()
        order_description += "\n"
    data.append(order_description)
    data.append(price)
    data.append(order_date)
    data.append(order_time)
    data.append(duration)
    data.append(status)
    orders.append_row(data)


def update_order_status():
    """
    Update status for the orders that overcome the estimated time
    """
    orders = SHEET.worksheet("orders")
    orders_list = orders.get_all_values()

    # get current time
    tz_dublin = pytz.timezone('Europe/Dublin')
    now = datetime.now(tz_dublin)
    current_time = now.strftime("%H:%M")

    for idx, row in enumerate(orders_list[1:]):
        # convert sheet string time into datetime format
        order_time = datetime.strptime(row[4], '%H:%M')
        # add duration in minutes to order time
        time_plus_duration = order_time + timedelta(minutes=int(row[5]))
        # check if current time overcomes order time plus duration
        if time_plus_duration < datetime.strptime(current_time, '%H:%M'):
            orders.update_cell(idx + 2, 7, "Ready")


def main():
    """
    Run all program functions
    """
    class PizzaOrder:
        """
        Creates an instance of PizzaOrder
        """
        def __init__(self, p_type, size, sauce, cheese, topings, quantity,
                     price, prep_time):
            self.p_type = p_type
            self.size = size
            self.sauce = sauce
            self.cheese = cheese
            self.topings = topings
            self.quantity = quantity
            self.price = price
            self.prep_time = prep_time

        def get_string(self):
            """ Generates a string that includes the order details"""
            if self.sauce == " ":
                # generate string for custom pizza
                pizza_string = f"{self.quantity} X {self.size} {self.p_type} "
                if int(self.quantity) > 1:
                    pizza_string += "pizzas"
                else:
                    pizza_string += "pizza"

                return pizza_string
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
    orders_refference = []
    # create loops so the user have the possibility to return to the previous
    # steps when user's input = "B" and restart the order when
    # user's input = "R"
    while True:
        # if user choose restart the orders list is emptied
        if add_to_order is False:
            orders_list = []
        # gets pizza type code
        pizza_type = display_pizza_menu(orders_list)

        # gets pizza type code
        pizza_size = display_pizza_sizes()
        while pizza_size.upper() == "B":
            pizza_type = display_pizza_menu(orders_list)
            pizza_size = display_pizza_sizes()

        # gets pizza custom values codes if user choose 6
        if pizza_type == "6":
            custom_pizza_values = get_values_for_custom_pizza()

            # restart loop
            if custom_pizza_values[len(custom_pizza_values)-1] == "restart":
                continue
        else:
            custom_pizza_values = " "

        # gets pizza quantity
        pizza_quantity = get_pizza_quantity()
        if pizza_quantity.upper() == "R":
            add_to_order = False
            continue
        # gets pizza codes strings from worksheets
        sheet_values = get_sheet_values(pizza_type, pizza_size,
                                        custom_pizza_values)
        p_type = sheet_values[0]
        size = sheet_values[1]
        sauce = sheet_values[2]
        cheese = sheet_values[3]
        topings = sheet_values[4]
        unit_price = sheet_values[5]
        prep_time = sheet_values[6]

        # creates a instance of the order
        order = PizzaOrder(p_type, size, sauce, cheese, topings,
                           pizza_quantity, int(pizza_quantity) * unit_price,
                           int(pizza_quantity) * prep_time)
        # adds the instance to the orders list
        orders_list.append(order)

        # display order details
        finalize_order_value = finalize_order(orders_list)
        if finalize_order_value.upper() == "A":
            add_to_order = True
            continue
        elif finalize_order_value.upper() == "R":
            add_to_order = False
            continue

        # get today date
        today = date.today()
        order_date = today.strftime("%d/%m/%Y")

        # get order time
        tz_dublin = pytz.timezone('Europe/Dublin')
        now = datetime.now(tz_dublin)
        order_time = now.strftime("%H:%M")

        # get refferences from worksheet and generate a new one
        orders_refference = get_sheet_order_refference()
        order_refference = generate_order_refference(orders_refference)

        # get total order duration in minutes
        duration_in_minutes = get_total_duration(orders_list)

        # update orders worksheet
        update_orders(order_refference, orders_list,
                      get_total_price(orders_list),
                      order_date, order_time,
                      duration_in_minutes, "Preparing")

        # get string format for duration
        duration_string = get_duration_string(duration_in_minutes)

        # display order refference and final menu
        final_menu_value = final_menu(order_refference, duration_string)
        if final_menu_value.upper() == "R":
            add_to_order = False
            continue
        else:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print(colored("Hope to see you soon!", "yellow"))
            update_order_status()

        break


main()
