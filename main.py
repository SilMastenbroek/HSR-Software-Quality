import sys
import os

# Voeg de src-map toe aan het pad zodat Python Views, Controllers, Models kan vinden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Startpunt van de applicatie
from Views.user_interface import main_menu

if __name__ == "__main__":
    main_menu()