"""
extract.py

This script extracts and displays information about nodes relevant to a specific class in a decision tree.

Usage:
    python extract.py <target_class> [--verbose] [--json FILENAME]

Arguments:
    target_class    The name of the class to extract information for.
    --verbose       (Optional) If present, prints detailed information about each relevant node.
    --json FILENAME (Optional) Path to the JSON file containing the decision tree data.
                    Defaults to 'decision_tree_table.json' in the current directory.

The script reads a decision tree structure from the specified JSON file (or 'decision_tree_table.json' by default).
It then finds all nodes where the probability of the target class is non-zero.

In non-verbose mode, it outputs a comma-separated list of relevant node IDs.
In verbose mode, it provides detailed information about each relevant node, including:
    - Node ID
    - Split feature and threshold (for non-leaf nodes)
    - Probability for the target class
    - Full probability distribution for all classes at that node

This tool is useful for analyzing the presence and distribution of a specific class throughout a decision tree.

Example usage:
    python extract.py "Combretaceae"
    python extract.py "Combretaceae" --verbose
    python extract.py "Combretaceae" --json my_tree.json
"""

import sys
import json
import argparse

def load_tree_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def find_class_nodes(tree_data, target_class):
    nodes = tree_data['nodes']
    classes = tree_data['classes']
    features = tree_data['features']

    try:
        target_class_index = classes.index(target_class)
    except ValueError:
        print(f"Class '{target_class}' not found in the decision tree.")
        return []

    relevant_nodes = []
    for node in nodes:
        prob = node['prob_map'][0][target_class_index]
        if prob > 0:
            relevant_nodes.append((node['node_id'], prob, node))

    return relevant_nodes

def print_class_nodes(relevant_nodes, features, verbose):
    if verbose:
        print(f"Nodes relevant to class '{target_class}':")
        for node_id, prob, node in relevant_nodes:
            print(f"Node ID: {node_id}")
            if node['feature'] is not None:
                feature_name = features[node['feature']]
                print(f"  Split on: '{feature_name}' <= {node['threshold']}")
            else:
                print("  Leaf node")
            print(f"  Probability for target class: {prob:.4f}")
            print(f"  Full probability map: {node['prob_map'][0]}")
            print()
    else:
        node_ids = [str(node_id) for node_id, _, _ in relevant_nodes]
        print(','.join(node_ids))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="[Description of the script]")
    parser.add_argument("target_class", help="The target class to find relevant nodes for")  # Only for extract.py
    parser.add_argument("--verbose", action="store_true", help="Print detailed information about each node")
    parser.add_argument("--json", default="decision_tree_table.json", help="Path to the JSON file containing the decision tree data")
    parser.add_argument("--vocab", default="vocab.json", help="Path to the vocabulary JSON file")
    args = parser.parse_args()

    try:
        tree_data = load_tree_from_json(args.json)
    except FileNotFoundError:
        print(f"Error: JSON file '{args.json}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.json}' is not a valid JSON file.")
        sys.exit(1)

    
    target_class = args.target_class
    relevant_nodes = find_class_nodes(tree_data, target_class)
    
    if relevant_nodes:
        print_class_nodes(relevant_nodes, tree_data['features'], args.verbose)
    else:
        print(f"No nodes found with non-zero probability for class '{target_class}'. Perhaps you need to make a vague search with vague search file")
        from vague_search_edit_d import vague_search, load_words_from_json

        word_list = load_words_from_json(args.vocab)
        results = vague_search(target_class, word_list, 5)

        print(f"Top 5 results for '{target_class}':")
        for word, distance in results:
            print(f"{word}: {distance}")
