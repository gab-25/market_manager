from market_manager.constants import VERSION
from market_manager.product import Product
from market_manager import data


def add_product(name: str = None, amount: int = None, purchase_price: float = None, selling_price: float = None):
    """
    Adds a product to the market.
    """
    try:
        name = name or input("Nome del prodotto: ")
        if len(name) == 0:
            raise ValueError
        amount = amount or int(input("Quantità: "))
        product = data.get_product(name)
        if product is None:
            purchase_price = purchase_price or float(input("Prezzo di acquisto: "))
            selling_price = selling_price or float(input("Prezzo di vendita: "))
    except ValueError:
        print("Errore: valore non valido!")
        add_product(name=name, amount=amount, purchase_price=purchase_price, selling_price=selling_price)
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

    close_shop = False
    while not close_shop:
        try:
            name = input("Nome del prodotto: ")
            amount = int(input("Quantità: "))
            product = data.get_product(name)
            if product is None:
                raise ValueError
            product.amount -= amount
            data.save_product(product)

            registered_sale.append((amount, product.name, product.selling_price))

            close_shop = input("Aggiungere un altro prodotto ? (si/NO)") == "si"
        except ValueError:
            print("Errore: prodotto non in magazzino!")

    print("VENDITA REGISTRATA")
    for sale in registered_sale:
        print(f"- {sale[0]} X {sale[1]}: €{sale[2]}")
    total_sale = sum(sale[0] for sale in registered_sale)
    print(f"Totale: €{total_sale}")


def list_products():
    """
    Lists all products in the market.
    """
    print("Prodotti in magazzino:")
    print("PRODOTTO\tQUANTITA'\tPREZZO")
    for product in data.get_products():
        print(f"{product.name}\t{product.amount}\t€{product.selling_price}\n")


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


def _main():
    """
    Main function.
    """
    print(f"""
 __  __            _        _     __  __                                   
|  \/  |          | |      | |   |  \/  |                                  
| \  / | __ _ _ __| | _____| |_  | \  / | __ _ _ __   __ _  __ _  ___ _ __ 
| |\/| |/ _` | '__| |/ / _ \ __| | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
| |  | | (_| | |  |   <  __/ |_  | |  | | (_| | | | | (_| | (_| |  __/ |   
|_|  |_|\__,_|_|  |_|\_\___|\__| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                            __/ |          
                                                            |___/           
v{VERSION}
""")

    while True:
        try:
            command = input("Inserisci un comando: ")

            if command == "aiuto" or command not in ["aggiungi", "vendita", "elenca", "chiudi"]:
                if command != "aiuto":
                    print("Errore: comando non valido!")
                print_help()
                continue

            if command == "aggiungi":
                add_product()
                print("Prodotto aggiunto!\n")

            if command == "vendita":
                shop_products()

            if command == "elenca":
                list_products()

            if command == "chiudi":
                print("Bye bye!\n")
                break
        except KeyboardInterrupt:
            print("\nBye bye!\n")
            break


if __name__ == "__main__":
    _main()
