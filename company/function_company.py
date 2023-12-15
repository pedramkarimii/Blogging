import json
from company_data import *
import pandas as pd


def calculate_markup_percent(product_type, product_number):
    """Calculate markup percentage for a product based on quantity.

    Args:
        product_type (str): The type of the product.
        product_number (int): The quantity of the product.

    Returns:
        float or str: Calculated markup percentage or an error message.
    """
    for markup_info in markup_list:
        if markup_info['product_type'] == product_type:
            lower_cost = markup_info['lower_cost']
            upper_cost = markup_info['upper_cost']
            lower_count = markup_info['lower_count']

            if product_number == 1:
                return upper_cost

            elif product_number >= lower_count:
                return lower_cost

            elif 1 <= product_number <= lower_count:
                proportion = (product_number - 1) / (lower_count - 1)
                markup_percent = upper_cost - (upper_cost - lower_cost) * proportion
                return markup_percent

    return f"Invalid product type: {product_type}"


def calculate_product_price_without_discount(product_type, count):
    """
    Calculate product price without considering user-specific discount.

    Args:
        product_type (str): The type of the product.
        count (int): The quantity of the product.

    Returns:
        dict or str: Calculated product details or an error message.
    """
    for product_info in product_list:
        if product_info['type'] == product_type:
            product_name = product_info['name']
            markup_percent = calculate_markup_percent(product_type, count)
            total_price = count * product_info['price']

            commission = total_price * (markup_percent / 100)
            total_with_commission = total_price + commission

            return {
                "product_name": product_name,
                "total_price": total_price,
                "total_with_commission": total_with_commission,
                "discount": f"{0}%"

            }

    return f"Invalid product type: {product_type}"


def calculate_discount(product_type, total_price, user_id):
    """
    Calculate discount based on user ID and product information.

    Args:
        product_type (str): The type of the product.
        total_price (float): The total price of the product.
        user_id (int or None): The user ID for discount calculation.

    Returns:
        float: Calculated total discount.
    """

    if user_id is None:
        return 0

    user_discounts = [discount for discount in discount_list if user_id in discount['users']]
    discount_amount = 0
    discount_percentage = 0
    sum_percent = []
    sum_dollar = []

    for product_info in product_list:
        if product_info['type'] == product_type:
            for discount in user_discounts:
                if discount['group_name'] in product_info.get('commission_groups', []):
                    if discount['unit'] == 'percent':
                        discount_percentage += discount['cost']
                        discount_percent1 = (discount_percentage / 100) * total_price
                        discount_percent2 = total_price - discount_percent1
                        sum_ = total_price - discount_percent2
                        sum_percent.append(sum_)

                    elif discount['unit'] == 'Dollar':
                        discount_amount += discount['cost']
                        discount_dollar = total_price - discount_amount
                        sum_ = total_price - discount_dollar
                        sum_dollar.append(sum_)

            for discount in user_discounts:
                if discount['group_name'] in product_info.get('commission_groups'):
                    if discount['unit'] == 'Dollar' or discount['unit'] == 'percent':
                        for percent in sum_percent:
                            result_percent = percent
                            for dollar in sum_dollar:
                                result_dollar = dollar
                                return (total_price - result_percent) - result_dollar
                    elif discount['unit'] == 'percent':
                        for percent in sum_percent:
                            return total_price - percent

                    elif discount['unit'] == 'Dollar':
                        for dollar in sum_dollar:
                            return total_price - dollar
            return total_price


def calculate_product_price_with_discount(product_type, count, user_id):
    """
    Calculate product price with user-specific discount.

    Args:
        product_type (str): The type of the product.
        count (int): The quantity of the product.
        user_id (int or None): The user ID for personalized calculations.

    Returns:
        dict or str: Calculated product details or an error message.
    """
    for product_info in product_list:
        if product_info['type'] == product_type:
            product_name = product_info['name']
            total_price = count * product_info['price']
            markup_percent = calculate_markup_percent(product_type, count)
            commission = total_price * (markup_percent / 100)
            total_with_commission = total_price + commission

            total_with_discount = calculate_discount(product_type, total_with_commission, user_id)
            discount = total_with_commission - (total_with_discount or total_with_commission)

            if user_id is not None:
                user_info = next((user for user in user_list if user['userid'] == user_id), None)
                if user_info:
                    return {

                        "product_name": product_name,
                        "total_price": total_price,
                        "total_with_commission": round(total_with_commission, 2),
                        "total_with_discount": f"{round(total_with_discount, 2)}",
                        "discount": f"{round(discount, 2)}%",
                        "username": {
                            "first_name": user_info["first_name"],
                            "last_name": user_info["last_name"]
                        }
                    }
                else:
                    print("The discount is not for you")

            return {
                "product_name": product_name,
                "total_price": total_price,
                "total_with_commission": total_with_commission,
                "total_with_discount": total_with_discount,
            }


    return f"Invalid product type: {product_type}"


def debug_info():
    """Display product and user information."""
    print("Product List:")
    Display_product_list = pd.DataFrame(product_list)
    print(Display_product_list)

    print("\nUser List:")
    Display_user_list = pd.DataFrame(user_list)
    print(Display_user_list)


# Main program loop
purchases = []  # List to store purchases
user_id = None  # Initialize user_id outside the try-except block
product_type = None  # Initialize product_type outside the try-except block
count = None  # Initialize count outside the try-except block
try:
    if __name__ == "__main__":
        while True:
            print(
                "-------------------------------------------------------------------------------------------------")
            print("Options:")
            print("1. Product purchase")
            print("2. Buying products for special people")
            print("3. Display Product and User information")
            print("4. Save product and user purchases")
            print("5. Exit")
            option = input("Enter option (1-5): ")
            print(
                "-------------------------------------------------------------------------------------------------")

            option = int(option)
            if option not in range(1, 6):
                print("Invalid option. Please enter a number between 1 and 5.")
                continue
            elif option == 1:
                """
                Calculate product price without considering user-specific discount.
                """
                product_type = input("Enter product type: ")
                count = int(input("Enter quantity: "))
                if count < 0:
                    raise ValueError
                elif count == float:
                    raise ValueError
                result = calculate_product_price_without_discount(product_type, count)
                print(result)
                user_purchase = {
                    "user_id": user_id,
                    "product_type": product_type,
                    "count": count,
                    "product_details": calculate_product_price_without_discount(product_type, count)}
                purchases.append(user_purchase)
            elif option == 2:
                user_id = int(input("Enter user ID: "))
                # user_id = input(user_id) if option == 2 else None
                """
                Calculate product price with user-specific discount.
                """
                product_type = input("Enter product type: ")
                count = int(input("Enter quantity: "))

                if count < 0:
                    raise ValueError
                elif count == float:
                    raise ValueError

                result = calculate_product_price_with_discount(product_type, count, user_id)
                print(result)
                user_purchase = {
                    "user_id": user_id,
                    "product_type": product_type,
                    "count": count,
                    "product_details": calculate_product_price_with_discount(product_type, count, user_id)}
                purchases.append(user_purchase)
            elif option == 3:
                """
                Display product information.
                """
                debug_info()
            elif option == 4:
                """
                Save the current product and user purchases.
                """
                with open("information.txt", "w") as json_file:
                    json.dump(purchases, json_file, indent=2)
                    print("Product and user purchase saved.")

            elif option == 5:
                """
                Exit the program.
                """
                print("Exiting program.")
                break

except ValueError:
    print("Invalid input. Please enter valid input values.")
    print("-------------------------------------------------------------------------------------------------------")
