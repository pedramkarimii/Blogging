import json
from company_data import *
import pandas as pd


# MarkupMixin calculates markup percentages
class MarkupMixin:
    """Calculate markup percentage based on product type and quantity.
    product_type: Type of the product
    product_number: Quantity of the product
    return: Calculated markup percentage or an error message"""

    def calculate_markup_percent(self, product_type, product_number):
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


# DiscountMixin calculates discounts
class DiscountMixin:
    """Calculate discounts based on product type, total price, and user ID.
    product_type: Type of the product
    total_price: Total price of the product
    user_id: ID of the user
    return: Calculated discount amount or percentage"""

    def calculate_discount(self, product_type, total_price, user_id):
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
                    if discount['group_name'] in product_info.get('commission_groups'):
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
                        if discount['unit'] == 'percent':
                            for percent in sum_percent:
                                return total_price - percent

                        elif discount['unit'] == 'Dollar':
                            for dollar in sum_dollar:
                                return total_price - dollar
                return total_price


# ProductMixin combines DiscountMixin and MarkupMixin
class ProductMixin(DiscountMixin, MarkupMixin):
    """Calculate total price, commission, and discounts for a product.
    product_type: Type of the product
    count: Quantity of the product
    user_id: ID of the user (optional)
    return: Dictionary with calculated details or an error message"""

    def calculate_product_price(self, product_type, count, user_id=None):
        for product_info in product_list:
            if product_info['type'] == product_type:
                product_name = product_info['name']
                markup_percent = self.calculate_markup_percent(product_type, count)
                total_price = count * product_info['price']
                commission = total_price * (markup_percent / 100)
                total_with_commission = total_price + commission
                discount = self.calculate_discount(product_type, total_with_commission, user_id)
                total_with_discount = total_with_commission - (discount or total_with_commission)
                if user_id is not None:
                    user_info = next((user for user in user_list if user['userid'] == user_id), None)
                    if user_info:
                        return {
                            "product_name": product_name, "total_price": total_price,
                            "total_with_commission": round(total_with_commission, 2),
                            "total_with_discount": round(discount, 2),
                            "discount": f"{round(total_with_discount, 2)}%",
                            "username": {
                                "first_name": user_info["first_name"],
                                "last_name": user_info["last_name"]}}
                return {"product_name": product_name, "total_price": total_price,
                        "total_with_commission": total_with_commission, "discount": f"{discount}%"}
        return f"Invalid product type: {product_type}"


# DebugMixin provides debugging information
class DebugMixin:
    """Print information about products and users for debugging."""
    def debug_info(self):
        """Display product and user information."""
        print("Product List:")
        Display_product_list = pd.DataFrame(product_list)
        print(Display_product_list)

        print("\nUser List:")
        Display_user_list = pd.DataFrame(user_list,)
        print(Display_user_list)


# PurchasesMixin handles saving purchases to a file
class PurchasesMixin:
    """Save product and user purchases to a file."""
    purchases = []

    def save_purchases(self):
        with open("information.txt", "w") as json_file:
            json.dump(self.purchases, json_file, indent=2)
        print("Product and user purchases saved.")


# Program class combines all mixins and runs the main program
class Program(ProductMixin, DiscountMixin, MarkupMixin, DebugMixin, PurchasesMixin):
    """Run the main program with a menu"""
    def run(self):
        while True:
            try:
                print(
                    "-------------------------------------------------------------------------------------------------")
                print("Options:")
                print(
                    "1.Product purchase\n2.Buying products for special people\n3.Display Product and User information\n"
                    "4.Save product and user purchases\n5.Exit\n")
                option = input("Enter option (1-5): ")
                print(
                    "-------------------------------------------------------------------------------------------------")
                option = int(option)
                if option not in range(1, 6):
                    print("Invalid option. Please enter a number between 1 and 5.")
                    continue
                elif option == 1 or option == 2:
                    user_id_input = input("Enter user ID: ") if option == 2 else None
                    user_id = int(user_id_input.strip()) if user_id_input and user_id_input.strip() else None
                    product_type = input("Enter product type: ")
                    count = int(input("Enter quantity: "))
                    if count < 0:
                        raise ValueError
                    elif count == float:
                        raise ValueError
                    result = self.calculate_product_price(product_type, count, user_id)
                    print(result)
                    user_purchase = {"user_id": user_id, "product_type": product_type, "count": count,
                                     "product_details": self.calculate_product_price(product_type, count, user_id)}
                    self.purchases.append(user_purchase)
                elif option == 3:
                    self.debug_info()
                elif option == 4:
                    self.save_purchases()
                    print("Product and user purchase saved")
                    break
                elif option == '5':
                    print("Exiting program.")
                    break
            except ValueError:
                print("Invalid input. Please enter valid numeric values.")
                print(
                    "-------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    Program().run()
