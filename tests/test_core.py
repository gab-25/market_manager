import unittest
import io
from unittest.mock import patch
from market_manager.core import add_product, profit_products, shop_products, list_products, print_help
from market_manager import data
from market_manager.product import Product


class TestMarketManager(unittest.TestCase):
    """Test cases for the market manager."""

    def setUp(self):
        """Setup for test cases."""
        with patch("builtins.open"):
            self.product1 = Product("Apple", 10, 1.0, 1.5)
            self.product2 = Product("Banana", 5, 0.5, 0.8)
            data.save_product(self.product1)
            data.save_product(self.product2)

    def tearDown(self):
        """Cleanup after test cases."""
        data._database.clear()

    @patch("builtins.open")
    def test_add_product(self, mock_open):
        """Test adding a new product."""
        with patch("builtins.input", side_effect=["Orange", "-20", "20", "0.7", "1.0"]):
            add_product()
            product = data.get_product("Orange")
            self.assertIsNotNone(product)
            self.assertEqual(product.name, "Orange")
            self.assertEqual(product.amount, 20)
            self.assertEqual(product.purchase_price, 0.7)
            self.assertEqual(product.selling_price, 1.0)

    @patch("builtins.open")
    def test_add_existing_product(self, mock_open):
        """Test adding more of an existing product."""
        with patch("builtins.input", side_effect=["Apple", "-5", "5"]):
            add_product()
            product = data.get_product("Apple")
            self.assertEqual(product.amount, 15)

    @patch("builtins.open")
    def test_shop_products(self, mock_open):
        """Test shopping products."""
        with patch("builtins.input", side_effect=["Apple", "11", "3", "si", "Banana", "2", "no"]):
            shop_products()
            product1 = data.get_product("Apple")
            product2 = data.get_product("Banana")
            self.assertEqual(product1.amount - product1.pieces_sold, 7)
            self.assertEqual(product2.amount - product2.pieces_sold, 3)

    def test_list_products(self):
        """Test listing products."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            list_products()
            self.assertIn("Apple", mock_stdout.getvalue())
            self.assertIn("Banana", mock_stdout.getvalue())
            self.assertIn("10", mock_stdout.getvalue())
            self.assertIn("5", mock_stdout.getvalue())
            self.assertIn("€1.5", mock_stdout.getvalue())
            self.assertIn("€0.8", mock_stdout.getvalue())

    @patch("market_manager.data.get_products")
    def test_profit_products(self, mock_get_products):
        """Test calculating profits."""
        mock_get_products.return_value = [
            Product("Apple", 10, 1.0, 2.0, pieces_sold=5),
            Product("Banana", 5, 0.5, 1.5, pieces_sold=2),
        ]
        with patch("builtins.print") as mock_print:
            profit_products()
            self.assertIn("Profitto: lordo=€13.00 netto=€7.00", mock_print.call_args_list[0][0][0])

    def test_print_help(self):
        """Test printing help message."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_help()
            self.assertIn("aggiungi", mock_stdout.getvalue())
            self.assertIn("elenca", mock_stdout.getvalue())
            self.assertIn("vendita", mock_stdout.getvalue())
            self.assertIn("profitti", mock_stdout.getvalue())
            self.assertIn("aiuto", mock_stdout.getvalue())
            self.assertIn("chiudi", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
