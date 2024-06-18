import unittest
from unittest.mock import patch
from market_manager.data import (
    save_product,
    remove_product,
    get_product,
    get_products,
    _load_data,
    _save_data,
)
from market_manager.product import Product
from market_manager.constants import FILE_DATA


class DataTest(unittest.TestCase):
    def setUp(self):
        # Clear the database before each test
        _database.clear()

    def test_save_product(self):
        product = Product("Apple", 10, 1.0, 1.5)
        self.assertTrue(save_product(product))
        self.assertEqual(get_product("Apple"), product)

    def test_remove_product(self):
        product = Product("Banana", 5, 0.5, 0.8)
        save_product(product)
        self.assertTrue(remove_product("Banana"))
        self.assertIsNone(get_product("Banana"))

    def test_get_product(self):
        product = Product("Orange", 20, 0.75, 1.25)
        save_product(product)
        self.assertEqual(get_product("Orange"), product)

    def test_get_products(self):
        product1 = Product("Apple", 10, 1.0, 1.5)
        product2 = Product("Banana", 5, 0.5, 0.8)
        save_product(product1)
        save_product(product2)
        products = get_products()
        self.assertIn(product1, products)
        self.assertIn(product2, products)

    @patch("market_manager.data._save_data")
    def test_load_data(self, mock_save_data):
        # Mock the file reading behavior
        with patch("builtins.open", mock_open(read_data=csv_data)):
            _load_data()
            self.assertEqual(len(_database), 2)
            self.assertEqual(get_product("Apple").amount, 10)
            self.assertEqual(get_product("Banana").selling_price, 0.8)
            mock_save_data.assert_not_called()

    @patch("builtins.open")
    def test_save_data(self, mock_open):
        product1 = Product("Apple", 10, 1.0, 1.5)
        product2 = Product("Banana", 5, 0.5, 0.8)
        _database[product1.name] = product1
        _database[product2.name] = product2
        _save_data()
        mock_open.assert_called_once_with(FILE_DATA, "w", encoding="utf-8")
        # You'll need to assert the content written to the file here
        # using mock_open.return_value.write.assert_called_once_with(...)

    # ... Add more tests for edge cases and error handling ...


if __name__ == "__main__":
    unittest.main()
