import sys
from tabulate import tabulate
from market_manager import data
from market_manager.product import Product


def _input_valid_number(message, type_number):
    """
    Gets a valid number from the user.
    """
    while True:
        try:
            if type_number == "int":
                value = int(input(message))
            if type_number == "float":
                value = float(input(message))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Errore: valore non valido!")


def add_product():
    """
    Adds a product to the market.
    """
    try:
        name = input("Nome del prodotto: ")
        if len(name) == 0:
            raise ValueError
        amount = _input_valid_number("Quantità: ", "int")
        product = data.get_product(name)
        if product is None:
            purchase_price = _input_valid_number("Prezzo di acquisto: ", "float")
            selling_price = _input_valid_number("Prezzo di vendita: ", "float")
        print(f"AGGIUNTO: {amount} X {name}\n")
    except ValueError:
        print("Errore: valore non valido!")
    if product is None:
        product = Product(name, amount, purchase_price, selling_price)
    else:
        product.amount += amount
    data.save_product(product)


def shop_products():
    """
    Shop products from the market.
    """
    registered_sale = []

    open_shop = True
    while open_shop:
        try:
            name = input("Nome del prodotto: ")
            product = data.get_product(name)
            if product is None:
                raise ValueError
            amount = int(input("Quantità: "))
            product.pieces_sold += amount
            data.save_product(product)

            registered_sale.append((amount, product.name, product.selling_price))

            open_shop = input("Aggiungere un altro prodotto? (si/no) ") == "si"
        except ValueError:
            print("Errore: prodotto non in magazzino!")

    print("VENDITA REGISTRATA")
    for sale in registered_sale:
        print(f"- {sale[0]} X {sale[1]}: €{sale[2]:.2f}")
    total_sale = sum(sale[0] * sale[2] for sale in registered_sale)
    print(f"Totale: €{total_sale:.2f}\n")


def list_products():
    """
    Lists all products in the market.
    """
    print("Prodotti in magazzino:")
    filtered_products = list(filter(lambda x: x.amount - x.pieces_sold > 0, data.get_products()))
    tabular_data = list(map(lambda x: [x.name, x.amount - x.pieces_sold, f"€{x.selling_price}"], filtered_products))
    print(tabulate(tabular_data, headers=["PRODOTTO", "QUANTITA", "PREZZO"], tablefmt="plain", numalign="left"))
    print("")


def profit_products():
    """
    Calculates the profit of the market.
    """
    total_gross_profit = 0
    total_net_profit = 0
    for product in data.get_products():
        gross_profit = product.pieces_sold * product.selling_price
        net_profit = gross_profit - (product.pieces_sold * product.purchase_price)
        total_gross_profit += gross_profit
        total_net_profit += net_profit
    print(f"Profitto: lordo=€{total_gross_profit:.2f} netto=€{total_net_profit:.2f}\n")


def print_help():
    """
    Prints the help message.
    """
    print(
        "I comandi disponibili sono i seguenti:\n"
        "- aggiungi: aggiungi un prodotto al magazzino\n"
        "- elenca: elenca i prodotto in magazzino\n"
        "- vendita: registra una vendita effettuata\n"
        "- profitti: mostra i profitti totali\n"
        "- aiuto: mostra i possibili comandi\n"
        "- chiudi: esci dal programma\n"
    )


def main():
    """
    Main function.
    """
    command = input("Inserisci un comando: ")

    if command == "aiuto" or command not in ["aggiungi", "vendita", "elenca", "profitti", "chiudi"]:
        if command != "aiuto":
            print("Errore: comando non valido!")
        print_help()
        return

    if command == "aggiungi":
        add_product()

    if command == "vendita":
        shop_products()

    if command == "elenca":
        list_products()

    if command == "profitti":
        profit_products()

    if command == "chiudi":
        print("Bye bye!\n")
        sys.exit(0)
