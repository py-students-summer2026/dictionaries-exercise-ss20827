"""
Functions necessary for running a virtual cookie shop (extra credit).
See README.md for instructions.
Do not run this file directly.  Rather, run main.py instead.

This is the Extra Credit version.
"""

import csv

def bake_cookies(filepath):
    """
    Opens up the CSV data file from the path specified as an argument.
    - Each line in the file, except the first, is assumed to contain comma-separated information about one cookie.
    - Creates a dictionary with the data from each line.
    - Adds each dictionary to a list of all cookies that is returned.

    :param filepath: The path to the data file.
    :returns: A list of all cookie data, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    cookies = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue
            cookie = {
                'id': int(row[0]),
                'title': row[1],
                'description': row[2],
                'price': float(row[3].replace("$", "")),
                'sugar_free': row[4].strip().lower() == "true",
                'gluten_free': row[5].strip().lower() == "true",
                'contains_nuts': row[6].strip().lower() == "true"
            }
            cookies.append(cookie)
    return cookies

def ask_yes_no(prompt):
    valid_responses = ["yes", "y", "no", "n"]
    response = ""
    while response.lower() not in valid_responses:
        response = input(prompt)
        if response.lower() not in valid_responses:
            print("Please enter 'yes', 'y', 'no', 'n'.")
    return response.lower() in ["yes", "y"]


def welcome():
    """
    Prints a welcome message to the customer in the format:

      Welcome to the Python Cookie Shop!
      We feed each according to their need.

    """
    # write your code for this function below this line
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.")
    print()
    print("We'd hate to trigger an allergic reaction to your body. So please answer the following questions:")
    print()
    allergic_to_nuts = ask_yes_no("Are you allergic to nuts? ")
    allergic_to_gluten = ask_yes_no("Are you allergic to gluten? ")
    has_diabetes = ask_yes_no("Do you have diabetes? ")
    return {
        'allergic_to_nuts': allergic_to_nuts,
        'allergic_to_gluten': allergic_to_gluten,
        'has_diabetes': has_diabetes
    }

def filter_cookies(cookies, dietary_needs):
    suitable = []
    for cookie in cookies:
        if dietary_needs['allergic_to_nuts'] and cookie['contains_nuts']:
            continue
        if dietary_needs['allergic_to_gluten'] and not cookie['gluten_free']:
            continue
        if dietary_needs['has_diabetes'] and not cookie['sugar_free']:
            continue
        suitable.append(cookie)
    return suitable


def display_cookies(cookies, dietary_needs):
    """
    Prints a list of all cookies in the shop to the user.
    - Sample output - we show only two cookies here, but imagine the output continues for all cookiese:
        Here are the cookies we have in the shop for you:

          #1 - Basboosa Semolina Cake
          This is a This is a traditional Middle Eastern dessert made with semolina and yogurt then soaked in a rose water syrup.
          Price: $3.99

          #2 - Vanilla Chai Cookie
          Crisp with a smooth inside. Rich vanilla pairs perfectly with its Chai partner a combination of cinnamon ands ginger and cloves. Can you think of a better way to have your coffee AND your Vanilla Chai in the morning?
          Price: $5.50

    - If doing the extra credit version, ask the user for their dietary restrictions first, and only print those cookies that are suitable for the customer.

    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below this line
    suitable_cookies = filter_cookies(cookies, dietary_needs)
    restrictions = []
    if dietary_needs['allergic_to_nuts']:
        restrictions.append("nuts")
    if dietary_needs['allergic_to_gluten']:
        restrictions.append("gluten")
    if dietary_needs['has_diabetes']:
        restrictions.append("sugar")
    if restrictions:
        restriction_str = " or ".join(restrictions)
        print(f"\nHere are the cookies without {restriction_str} that we think you might like:\n")
    else:
        print("\nHere are the cookies we have in the shop for you:\n")
    if not suitable_cookies:
        print("Sorry we don't have any cookies that match your dietary needs at this time.\n")
        return
    for cookie in suitable_cookies:
        print(f"#{cookie['id']} - {cookie['title']}")
        print(f"{cookie['description']}")
        print(f"Price: ${cookie['price']:.2f}")
        print()
    return suitable_cookies

def get_cookie_from_dict(id, cookies):
    """
    Finds the cookie that matches the given id from the full list of cookies.

    :param id: the id of the cookie to look for
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: the matching cookie, as a dictionary
    """
    # write your code for this function below this line
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None


def solicit_quantity(id, cookies):
    """
    Asks the user how many of the given cookie they would like to order.
    - Validates the response.
    - Uses the get_cookie_from_dict function to get the full information about the cookie whose id is passed as an argument, including its title and price.
    - Displays the subtotal for the given quantity of this cookie, formatted to two decimal places.
    - Follows the format (with sample responses from the user):

        My favorite! How many Animal Cupcakes would you like? 5
        Your subtotal for 5 Animal Cupcake is $4.95.

    :param id: the id of the cookie to ask about
    :param cookies: a list of all cookies in the shop, where each cookie is represented as a dictionary.
    :returns: The quantity the user entered, as an integer.
    """
    # write your code for this function below this line
    cookie = get_cookie_from_dict(id, cookies)
    quantity = ""
    while not quantity.isnumeric():
        quantity = input(f"My favourite! How many {cookie['title']}s would you like? ")
    quantity = int(quantity)
    subtotal = cookie['price'] * quantity
    print(f"Your subtotal for {quantity} {cookie['title']} is ${subtotal:.2f}.")
    return quantity



def solicit_order(cookies, suitable_cookies):
    """
    Takes the complete order from the customer.
    - Asks over-and-over again for the user to enter the id of a cookie they want to order until they enter 'finished', 'done', 'quit', or 'exit'.
    - Validates the id the user enters.
    - For every id the user enters, determines the quantity they want by calling the solicit_quantity function.
    - Places the id and quantity of each cookie the user wants into a dictionary with the format
        {'id': 5, 'quantity': 10}
    - Returns a list of all sub-orders, in the format:
        [
          {'id': 5, 'quantity': 10},
          {'id': 1, 'quantity': 3}
        ]

    :returns: A list of the ids and quantities of each cookies the user wants to order.
    """
    # write your code for this function below this line
    order = []
    stop_words = ["finished", "done", "quit", "exit"]
    suitable_ids = [c['id'] for c in suitable_cookies]
    response = input("\nPlease enter the number of any cookie you would like to purchase: ")
    while response.lower() not in stop_words:
        if response.isnumeric():
            id = int(response)
            if id in suitable_ids:
                quantity = solicit_quantity(id, cookies)
                order.append({'id': id, 'quantity': quantity})
            else:
                print("Sorry, that is not a valid cookie id. Please try again.")
        else:
            print("Sorry, that is not a valid cookie id. Please try again.")
        response = input('\nPlease enter the number of any cookie you would like to purchase (type "finished" if finished with your order): ')
    return order


def display_order_total(order, cookies):
    """
    Prints a summary of the user's complete order.
    - Includes a breakdown of the title and quantity of each cookie the user ordereed.
    - Includes the total cost of the complete order, formatted to two decimal places.
    - Follows the format:

        Thank you for your order. You have ordered:

        -8 Animal Cupcake
        -1 Basboosa Semolina Cake

        Your total is $11.91.
        Please pay with Bitcoin before picking-up.

        Thank you!
        -The Python Cookie Shop Robot.

    """
    # write your code for this function below this line
    print("\nThank you for your order. You have ordered:\n")
    total = 0
    for sub_order in order:
        cookie = get_cookie_from_dict(sub_order['id'], cookies)
        print(f"-{sub_order['quantity']} {cookie['title']}")
        total = total + cookie['price'] * sub_order['quantity']
    print(f"\nYour total is ${total:.2f}.")
    print("Please pay with Bitcoin before picking-up.")
    print("\nThank you!")
    print("-The Python Cookie Shop Robot")


def run_shop(cookies):
    """
    Executes the cookie shop program, following requirements in the README.md file.
    - This function definition is given to you.
    - Do not modify it!

    :param cookies: A list of all cookies in the shop, where each cookie is represented as a dictionary.
    """
    # write your code for this function below here.
    dietary_needs = welcome()
    suitable_cookies = display_cookies(cookies, dietary_needs)
    if not suitable_cookies:
        print("We're sorry we couldn't serve you today. Please visit again!")
        return
    order = solicit_order(cookies, suitable_cookies)
    display_order_total(order, cookies)