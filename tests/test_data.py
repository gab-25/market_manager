import unittest
from unittest.mock import patch, mock_open
from market_manager.data import (
    save_product,
    remove_product,
    get_product,
    get_products,
    _load_data,
    _save_data,
    _database,
)
from market_manager.product import Product
from market_manager.constants import FILE_DATA


class DataTest(unittest.TestCase):
    """Test the data module"""

    def setUp(self):
        # Clear the database before each test
        _database.clear()

    @patch("builtins.open")
    def test_save_product(self, mock_open):
        """Test saving a product"""
        product = Product("Apple", 10, 1.0, 1.5)
        self.assertTrue(save_product(product))
        self.assertEqual(get_product("Apple"), product)

    @patch("builtins.open")
    def test_remove_product(self, mock_open):
        """Test removing a product"""
        product = Product("Banana", 5, 0.5, 0.8)
        save_product(product)
        self.assertTrue(remove_product("Banana"))
        self.assertIsNone(get_product("Banana"))

    @patch("builtins.open")
    def test_get_product(self, mock_open):
        """Test getting a product"""
        product = Product("Orange", 20, 0.75, 1.25)
        save_product(product)
        self.assertEqual(get_product("Orange"), product)

    @patch("builtins.open")
    def test_get_products(self, mock_open):
        """Test getting all products"""
        product1 = Product("Apple", 10, 1.0, 1.5)
        product2 = Product("Banana", 5, 0.5, 0.8)
        save_product(product1)
        save_product(product2)
        products = get_products()
        self.assertIn(product1, products)
        self.assertIn(product2, products)

    @patch("os.path.exists", return_value=True)
    @patch("market_manager.data._save_data")
    def test_load_data(self, mock_save_data, mock_exists):
        """Test loading data from CSV file"""
        # Mock the CSV file content
        CSV_DATA = (
            "name,amount,purchase_price,selling_price\n"
            "Apple,10,1.0,1.5\n"
            "Banana,5,0.5,0.8\n"
            "Orange,20,0.75,1.25\n"
        )
        with patch("builtins.open", mock_open(read_data=CSV_DATA)):
            _load_data()
            self.assertEqual(len(_database), 3)
            self.assertIn("Apple", _database)
            self.assertIn("Banana", _database)
            self.assertIn("Orange", _database)
            mock_save_data.assert_not_called()

    @patch("builtins.open")
    def test_save_data(self, mock_open):
        """Test saving data to CSV file"""
        product1 = Product("Apple", 10, 1.0, 1.5)
        product2 = Product("Banana", 5, 0.5, 0.8)
        _database[product1.name] = product1
        _database[product2.name] = product2
        _save_data()
        mock_open.assert_called_once_with(FILE_DATA, "w", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
