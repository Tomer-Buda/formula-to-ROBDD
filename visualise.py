# visualise.py
import graphviz
import os

def render_bdd(manager, root_id, filename, var_names=None):
    """Draws the ROBDD using Graphviz."""
    dot = graphviz.Digraph(comment='ROBDD')
    dot.attr(rankdir='TB') 
    
    visited = set()
    queue = [root_id]
    visited.add(root_id)

    # Define Terminals
    dot.node('0', '0', shape='box', style='filled', fillcolor='#ffcccc') # Red
    dot.node('1', '1', shape='box', style='filled', fillcolor='#ccffcc') # Green

    while queue:
        curr = queue.pop(0)
        if curr in [manager.zero, manager.one]: 
            continue
        
        node = manager.nodes[curr]
        
        # Label with variable name if available
        label = var_names[node.var] if var_names else f"x{node.var}"
        dot.node(str(curr), label, shape='circle')

        # Draw Edges (Low=Dashed/Red, High=Solid/Blue)
        dot.edge(str(curr), str(node.low), label='0', style='dashed', color='red')
        if node.low not in visited:
            visited.add(node.low)
            queue.append(node.low)

        dot.edge(str(curr), str(node.high), label='1', style='solid', color='blue')
        if node.high not in visited:
            visited.add(node.high)
            queue.append(node.high)

    try:
        path = dot.render(filename, format='png', cleanup=True)
        print(f"Graph generated: {path}")
    except graphviz.backend.ExecutableNotFound:
        print("Error: Graphviz executable not found.")