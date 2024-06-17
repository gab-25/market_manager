class Product:
    """
    class to represent a product in the market.

    Attributes:
        name (str): name of the product
        amount (int): amount of the product
        purchase_price (float): purchase price of the product
        selling_price (float): selling price of the product
    """

    def __init__(self, name: str, amount: int, purchase_price: float, selling_price: float):
        self.name = name
        self.amount = amount
        self.purchase_price = purchase_price
        self.selling_price = selling_price

    def __dict__(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "purchase_price": self.purchase_price,
            "selling_price": self.selling_price,
        }
