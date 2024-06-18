import unittest
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
    def setUp(self):
        # Clear the database before each test
        data._database.clear()

    @patch("builtins.input", side_effect=["Apple", "10", "1.0", "1.5"])
    def test_add_product(self, mock_input):
        add_product()
        self.assertEqual(data.get_product("Apple").amount, 10)

    @patch("builtins.input", side_effect=["Apple", "5", "Banana", "2"])
    @patch("market_manager.data.get_product", side_effect=[Product("Apple", 15, 1.0, 1.5), None])
    def test_add_product_existing(self, mock_get_product, mock_input):
        add_product()
        self.assertEqual(data.get_product("Apple").amount, 20)

    @patch("builtins.input", side_effect=["Apple", "10", "si", "Banana", "5", "NO"])
    @patch(
        "market_manager.data.get_product", side_effect=[Product("Apple", 15, 1.0, 1.5), Product("Banana", 10, 0.5, 0.8)]
    )
    def test_shop_products(self, mock_get_product, mock_input):
        shop_products()
        self.assertEqual(data.get_product("Apple").amount, 5)
        self.assertEqual(data.get_product("Banana").amount, 5)

    @patch(
        "market_manager.data.get_products",
        return_value=[Product("Apple", 10, 1.0, 1.5), Product("Banana", 5, 0.5, 0.8)],
    )
    def test_list_products(self, mock_get_products):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            list_products()
            self.assertIn("Apple\t10\t€1.5", mock_stdout.getvalue())
            self.assertIn("Banana\t5\t€0.8", mock_stdout.getvalue())

    def test_print_help(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_help()
            self.assertIn("aggiungi: aggiungi un prodotto al magazzino", mock_stdout.getvalue())
            self.assertIn("vendita: registra una vendita effettuata", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["aggiungi", "Apple", "10", "1.0", "1.5", "chiudi"])
    def test_main_add_product(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Prodotto aggiunto!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["vendita", "Apple", "5", "NO", "chiudi"])
    @patch("market_manager.data.get_product", return_value=Product("Apple", 15, 1.0, 1.5))
    def test_main_shop_products(self, mock_get_product, mock_input):
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

    @patch("builtins.input", side_effect=["aggiungi", "", "10", "1.0", "1.5", "chiudi"])
    def test_add_product_empty_name(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Errore: valore non valido!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["vendita", "NonExistingProduct", "5", "NO", "chiudi"])
    @patch("market_manager.data.get_product", return_value=None)
    def test_shop_products_non_existing_product(self, mock_get_product, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _main()
            self.assertIn("Errore: prodotto non in magazzino!", mock_stdout.getvalue())
            self.assertIn("Bye bye!", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
