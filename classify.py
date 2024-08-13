"""
classify.py

This script provides an interactive interface for classifying samples using a pre-trained decision tree.

Usage:
    python classify.py [--verbose]

Arguments:
    --verbose       (Optional) If present, prints detailed probability distributions at each node.

The script reads a decision tree structure from a JSON file named 'decision_tree_table.json' in the same directory.
It then guides the user through the decision tree by asking questions based on the features at each node.

In non-verbose mode, it shows only the most probable class at each step.
In verbose mode, it displays the full probability distribution for all classes at each node.

The classification process continues until a leaf node is reached or the user chooses to end the session.

Features:
    - Interactive navigation through the decision tree
    - Option to go back to the previous node
    - Displays feature names and thresholds for easy interpretation
    - Verbose mode for detailed probability information

This tool is useful for understanding how the decision tree classifies samples and for making manual classifications.

Example usage:
    python classify.py
"""


import json

def load_tree_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def print_node_info(node, classes, features, verbose):
    print(f"Node {node['node_id']}:")
    if node['feature'] is not None:
        feature_name = features[node['feature']]
        print(f"Feature '{feature_name}' <= {node['threshold']}?")
    
    if verbose:
        print("Probability map:")
        for cls, prob in zip(classes, node['prob_map'][0]):
            print(f"  Class {cls}: {prob:.4f}")
    else:
        max_prob_index = max(range(len(node['prob_map'][0])), key=lambda i: node['prob_map'][0][i])
        max_prob_class = classes[max_prob_index]
        max_prob = node['prob_map'][0][max_prob_index]
        print(f"Most probable class: {max_prob_class} (probability: {max_prob:.4f})")

def navigate_tree(tree_data, verbose=False):
    nodes = {node['node_id']: node for node in tree_data['nodes']}
    classes = tree_data['classes']
    features = tree_data['features']
    
    current_node_id = 0
    node_stack = []

    while True:
        current_node = nodes[current_node_id]
        print("\n" + "="*40)
        print_node_info(current_node, classes, features, verbose)
        
        if current_node['left'] is None and current_node['right'] is None:
            print("This is a leaf node.")
        
        action = input("Action (l: left, r: right, b: back, e: end, q: quit): ").lower()
        
        if action == 'l' and current_node['left'] is not None:
            node_stack.append(current_node_id)
            current_node_id = current_node['left']
        elif action == 'r' and current_node['right'] is not None:
            node_stack.append(current_node_id)
            current_node_id = current_node['right']
        elif action == 'b' and node_stack:
            current_node_id = node_stack.pop()
        elif action == 'e':
            print("\nReached end of decision path.")
            print_node_info(current_node, classes, features, True)  # Always print verbose at the end
            break
        elif action == 'q':
            print("Quitting the program.")
            break
        else:
            print("Invalid action or movement not possible.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="[Description of the script]")
    parser.add_argument("target_class", help="The target class to find relevant nodes for")  # Only for extract.py
    parser.add_argument("--verbose", action="store_true", help="Print detailed information about each node")
    parser.add_argument("--json", default="decision_tree_table.json", help="Path to the JSON file containing the decision tree data")
    args = parser.parse_args()

    try:
        tree_data = load_tree_from_json(args.json)
    except FileNotFoundError:
        print(f"Error: JSON file '{args.json}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.json}' is not a valid JSON file.")
        sys.exit(1)


    tree_data = load_tree_from_json(filename)
    
    verbose = input("Verbose mode? (y/n): ").lower() == 'y'
    navigate_tree(tree_data, verbose)