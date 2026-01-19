# bdd.py
class BDDNode:
    """Represents a node in the BDD graph."""
    def __init__(self, uid, var, low, high):
        self.id = uid
        self.var = var # Variable index
        self.low = low # ID of 'else' child
        self.high = high # ID of 'then' child

class BDDManager:
    """Manages the creation and operations of BDD nodes."""
    def __init__(self, num_vars):
        self.unique_table = {} # (var, low, high) -> id
        self.computed_table = {} # (op, u, v) -> id
        self.nodes = {} # id -> BDDNode
        self.num_vars = num_vars
        self.node_counter = 2

        # Terminals: 0 and 1
        self.zero = 0
        self.one = 1
        self.nodes[0] = BDDNode(0, num_vars, None, None)
        self.nodes[1] = BDDNode(1, num_vars, None, None)

    def get_node(self, var, low, high):
        """Returns a canonical node for (var, low, high)."""
        if low == high: 
            return low
        
        key = (var, low, high)
        if key in self.unique_table: 
            return self.unique_table[key]

        uid = self.node_counter
        self.node_counter += 1
        self.nodes[uid] = BDDNode(uid, var, low, high)
        self.unique_table[key] = uid
        return uid

    def apply(self, op, u, v):
        """Applies a boolean operator to nodes u and v."""
        if (op, u, v) in self.computed_table: 
            return self.computed_table[(op, u, v)]

        u_node = self.nodes[u]
        v_node = self.nodes[v]

        # Base case: both are terminals
        if u_node.var == self.num_vars and v_node.var == self.num_vars:
            res = self.one if op(u == 1, v == 1) else self.zero
            return res

        # Shannon Expansion
        top_var = min(u_node.var, v_node.var)

        low_u = u_node.low if u_node.var == top_var else u
        high_u = u_node.high if u_node.var == top_var else u
        
        low_v = v_node.low if v_node.var == top_var else v
        high_v = v_node.high if v_node.var == top_var else v

        res_low = self.apply(op, low_u, low_v)
        res_high = self.apply(op, high_u, high_v)

        res = self.get_node(top_var, res_low, res_high)
        self.computed_table[(op, u, v)] = res
        return res