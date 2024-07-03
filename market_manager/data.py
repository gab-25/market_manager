import csv
import os
from market_manager.product import Product
from market_manager.constants import FILE_DATA


_database: dict[str, Product] = {}


def _load_data() -> None:
    """
    Load data from the file.
    """
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    row["name"],
                    int(row["amount"]),
                    float(row["purchase_price"]),
                    float(row["selling_price"]),
                    int(row["pieces_sold"]),
                )
                _database[product.name] = product


def _save_data() -> None:
    """
    Save data to the file.
    """
    with open(FILE_DATA, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "amount", "purchase_price", "selling_price", "pieces_sold"])
        writer.writeheader()
        for product in _database.values():
            writer.writerow(product.__dict__)


def save_product(product: Product) -> bool:
    """
    Add a product to the database.
    
    Parameters:
        product (Product): The product to add.
    Returns:
        bool: True if the product was added successfully, False otherwise.
    """
    _database[product.name] = product
    _save_data()
    return True


def remove_product(name: str) -> bool:
    """
    Remove a product from the database.

    Parameters:
        name (str): The name of the product to remove.
    Returns:
        bool: True if the product was removed successfully, False otherwise.
    """
    if name not in _database:
        return False
    del _database[name]
    _save_data()
    return True


def get_product(name: str) -> Product:
    """
    Get a product from the database.

    Parameters:
        name (str): The name of the product to get.
    Returns:
        Product: The product with the given name.
    """
    return _database.get(name)


def get_products() -> list[Product]:
    """
    Get all products in the database.
    """
    return list(_database.values())


_load_data()
