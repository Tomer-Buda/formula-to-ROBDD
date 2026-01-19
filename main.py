import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from formula_parser import build_bdd_from_string
from visualise import render_bdd

if __name__ == "__main__":
    # Get Formula
    user_input = input("Enter formula (e.g. 'a & b | c'): ")
    if not user_input.strip():
        print("No input provided.")
        exit()

    # Get Variable Order
    print("\nVariable Order determines the structure of the graph.")
    print("Example for comparator: a,b,c")
    order_input = input("Enter variable order (comma separated) OR press Enter for default: ")
    
    custom_order = None
    if order_input.strip():
        # Split by comma and strip spaces: "a, b, c" -> ['a', 'b', 'c']
        custom_order = [v.strip() for v in order_input.split(',') if v.strip()]

    print("\nBuilding BDD...")

    try:
        # Pass the inputs to the parser
        mgr, root, names = build_bdd_from_string(user_input, custom_order)

        if mgr:
            filename = "bdd_output"
            print(f"Generating graph as '{filename}.png'...")
            render_bdd(mgr, root, filename, var_names=names)
            print(f"Success! Open '{filename}.png' to view.")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")