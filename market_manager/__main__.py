from market_manager.constants import VERSION
from market_manager.core import add_product, list_products, print_help, profit_products, shop_products


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

            if command == "aiuto" or command not in ["aggiungi", "vendita", "elenca", "profitti", "chiudi"]:
                if command != "aiuto":
                    print("Errore: comando non valido!")
                print_help()
                continue

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
                break
        except KeyboardInterrupt:
            print("\nBye bye!\n")
            break


if __name__ == "__main__":
    _main()
