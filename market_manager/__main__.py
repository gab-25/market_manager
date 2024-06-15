from market_manager.constants import VERSION
from market_manager.product import Product
from market_manager import data


def _add_product(name: str = None, amount: int = None, purchase_price: float = None, selling_price: float = None):
    """
    Adds a product to the market.
    """
    try:
        name = name or input("Nome del prodotto: ")
        amount = amount or int(input("Quantità: "))
        purchase_price = purchase_price or float(input("Prezzo di acquisto: "))
        selling_price = selling_price or float(input("Prezzo di vendita: "))
    except ValueError:
        print("Errore: valore non valido!")
        _add_product(name=name, amount=amount, purchase_price=purchase_price, selling_price=selling_price)
    product = Product(name, amount, purchase_price, selling_price)
    data.add_product(product)


def _shop_products():
    pass


def _list_products():
    """
    Lists all products in the market.
    """
    pass


def _print_help():
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


print("""

  __  __            _        _     __  __                                   
 |  \/  |          | |      | |   |  \/  |                                  
 | \  / | __ _ _ __| | _____| |_  | \  / | __ _ _ __   __ _  __ _  ___ _ __ 
 | |\/| |/ _` | '__| |/ / _ \ __| | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |  | | (_| | |  |   <  __/ |_  | |  | | (_| | | | | (_| | (_| |  __/ |   
 |_|  |_|\__,_|_|  |_|\_\___|\__| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                             __/ |          
                                                            |___/           
v{version}
""".format(version=VERSION))

while True:
    try:
        command = input("Inserisci un comando: ")

        if command == "aiuto" or command not in ["aggiungi", "vendita", "elenca", "chiudi"]:
            if command != "aiuto":
                print("Errore: comando non valido!")
            _print_help()
            continue

        if command == "aggiungi":
            _add_product()
            print("Prodotto aggiunto!\n")

        if command == "vendita":
            _shop_products()

        if command == "elenca":
            _list_products()

        if command == "chiudi":
            print("Bye bye!\n")
            break
    except Exception as e:
        print("Errore:", e)
    except KeyboardInterrupt:
        print("\nBye bye!\n")
        break
