import unittest
import io
from unittest.mock import patch
from market_manager import data
from market_manager.product import Product
from market_manager.__main__ import (
    add_product,
    shop_products,
    list_products,
    print_help,
    _main,
)


class MainTest(unittest.TestCase):
    """Test the main function"""

    def setUp(self):
        # Clear the database before each test
        data._database.clear()

    @patch("builtins.open")
    @patch("builtins.input", side_effect=["Apple", "10", "1.0", "1.5"])
    def test_add_product(self, mock_input, mock_open):
        """Test the add_product function"""
        add_product()
        self.assertEqual(data.get_product("Apple").amount, 10)

    @patch("builtins.open")
    @patch("builtins.input", side_effect=["Apple", "5"])
    def test_add_product_existing(self, mock_input, mock_open):
        """Test the add_product function when the product already exists"""
        with patch("market_manager.data.get_product", side_effect=[Product("Apple", 15, 1.0, 1.5), None]):
            add_product()
        self.assertEqual(data.get_product("Apple").amount, 20)

    @patch("builtins.open")
    @patch("builtins.input", side_effect=["Apple", "10", "si", "Banana", "5", "no"])
    def test_shop_products(self, mock_input, mock_open):
        """Test the shop_products function"""
        with patch(
            "market_manager.data.get_product",
            side_effect=[Product("Apple", 15, 1.0, 1.5), Product("Banana", 10, 0.5, 0.8)],
        ):
            shop_products()
        self.assertEqual(data.get_product("Apple").amount, 5)
        self.assertEqual(data.get_product("Banana").amount, 5)

    @patch(
        "market_manager.data.get_products",
        return_value=[Product("Apple", 10, 1.0, 1.5), Product("Banana", 5, 0.5, 0.8)],
    )
    def test_list_products(self, mock_get_products):
        """Test the list_products function"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            list_products()
            self.assertIn("Apple\t10\t€1.5", mock_stdout.getvalue())
            self.assertIn("Banana\t5\t€0.8", mock_stdout.getvalue())

    def test_print_help(self):
        """Test the print_help function"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_help()
            self.assertIn("aggiungi: aggiungi un prodotto al magazzino", mock_stdout.getvalue())
            self.assertIn("vendita: registra una vendita effettuata", mock_stdout.getvalue())

    @patch("builtins.open")
    @patch("builtins.input", side_effect=["aggiungi", "Apple", "10", "1.0", "1.5", "chiudi"])
    def test_main_add_product(self, mock_input, mock_open):
        """Test the main function when adding a product"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Prodotto aggiunto!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.open")
    @patch("builtins.input", side_effect=["vendita", "Apple", "5", "no", "chiudi"])
    @patch("market_manager.data.get_product", return_value=Product("Apple", 15, 1.0, 1.5))
    def test_main_shop_products(self, mock_get_product, mock_input, mock_open):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("VENDITA REGISTRATA", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["elenca", "chiudi"])
    def test_main_list_products(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Prodotti in magazzino:", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["aiuto", "chiudi"])
    def test_main_print_help(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("I comandi disponibili sono i seguenti:", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["invalid_command", "chiudi"])
    def test_main_invalid_command(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Errore: comando non valido!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["", "chiudi"])
    def test_main_empty_command(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Errore: comando non valido!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
