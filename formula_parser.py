import re
from bdd import BDDManager

class BDDWrapper:
    """Helper class to overload Python operators."""
    def __init__(self, manager, node_id):
        self.mgr = manager
        self.id = node_id

    def __and__(self, other):
        return BDDWrapper(self.mgr, self.mgr.apply(lambda a, b: a and b, self.id, other.id))

    def __or__(self, other):
        return BDDWrapper(self.mgr, self.mgr.apply(lambda a, b: a or b, self.id, other.id))

    def __xor__(self, other):
        return BDDWrapper(self.mgr, self.mgr.apply(lambda a, b: a != b, self.id, other.id))

    def __invert__(self):
        return BDDWrapper(self.mgr, self.mgr.apply(lambda a, b: a != b, self.id, self.mgr.one))

def build_bdd_from_string(formula_str, custom_order=None):
    """
    Parses a string formula into a BDD.
    Args:
        formula_str (str): The boolean formula (e.g., "a & b")
        custom_order (list): Optional list of variable names in desired order (e.g. ['a', 'b'...])
    """
    # Identify all variables in the string
    found_vars = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', formula_str))
    
    # Determine the Order
    if custom_order:
        # Validate that the custom order covers all used variables
        missing = found_vars - set(custom_order)
        if missing:
            raise ValueError(f"Custom order is missing variables used in formula: {missing}")
        
        # Use the user's exact order
        final_vars = custom_order
    else:
        # Default: Alphabetical Sort
        final_vars = sorted(list(found_vars))

    # Create the variable map (Name -> Index)
    var_map = {name: i for i, name in enumerate(final_vars)}
    
    # Initialize Manager with enough variables
    manager = BDDManager(num_vars=len(final_vars))
    
    # Create BDD objects for eval()
    context = {}
    for name, index in var_map.items():
        node_id = manager.get_node(index, manager.zero, manager.one)
        context[name] = BDDWrapper(manager, node_id)

    # Evaluate
    try:
        # Pass the context so Python knows what "x1", "y1" etc refer to
        result_wrapper = eval(formula_str, {"__builtins__": None}, context)
        return manager, result_wrapper.id, final_vars
    except Exception as e:
        print(f"Parser Error: {e}")
        return None, None, None