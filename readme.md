Here's a concise enrichment of the README:

# Biology Classification

This project provides tools for classifying biological specimens using decision trees based on phenotypic data.

## Setup

1. Prepare your phenotype (X) and classification (y) data.
2. Train a decision tree model.
3. Use `data_formatting.ipynb` to convert the trained model to a JSON file.

## Tools

### classify.py

Interactive tool for classifying samples through the decision tree.

Usage:
```
python classify.py [--verbose] [--json FILENAME]
```

### extract.py

Extracts information about nodes relevant to a specific class in the decision tree.

Usage:
```
python extract.py <target_class> [--verbose] [--json FILENAME]
```

## Example Usage

Classify using the default JSON:
```
python classify.py --json decision_tree_table.json
```

Extract nodes for "Combretaceae" and save to file:
```
python extract.py "Combretaceae" --json decision_tree_table.json > Combretaceae.txt
```

Verbose extraction for "Combretaceae":
```
python extract.py "Combretaceae" --verbose --json decision_tree_table.json
```

## Features

- Interactive classification
- Node extraction for specific classes
- Verbose mode for detailed probability distributions
- Custom JSON file support

For more details, refer to the docstrings in each script.
