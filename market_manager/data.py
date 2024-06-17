import csv
import os
from market_manager.product import Product
from market_manager.constants import FILE_DATA


_database: dict[str, Product] = {}


def _load_data() -> None:
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(**row)
                _database[product.name] = product


def _save_data() -> None:
    products = list(_database.values())
    with open(FILE_DATA, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=products[0].__dict__.keys())
        writer.writeheader()
        for product in products:
            writer.writerow(product.__dict__)


def add_product(product: Product) -> bool:
    """
    Add a product to the database.
    """
    _database[product.name] = product
    _save_data()
    return True


def remove_product(product: Product) -> bool:
    """
    Remove a product from the database.
    """
    del _database[product.name]
    _save_data()
    return True


def get_product(name: str) -> Product:
    """
    Get a product from the database.
    """
    return _database[name]


def get_products() -> list[Product]:
    """
    Get all products in the database.
    """
    return list(_database.values())


_load_data()
