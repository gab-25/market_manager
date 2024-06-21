from market_manager.constants import VERSION
from market_manager.core import main


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
            main()
        except KeyboardInterrupt:
            print("\nBye bye!\n")
            break


if __name__ == "__main__":
    _main()
