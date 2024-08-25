import json
import argparse
import editdistance
import numpy as np

def load_words_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def vague_search(query, word_list, n=10):
    distances = list(map(lambda word: editdistance.eval(query, word), word_list))
    rank = np.argsort(distances)
    results = []
    for i in range(min(n, len(word_list))):
        results.append((word_list[rank[i]], distances[rank[i]]))
    return results

def main():
    parser = argparse.ArgumentParser(description="Perform vague search using edit distance.")
    parser.add_argument("query", help="The search query")
    parser.add_argument("--vocab", default="vocab.json", help="Path to the vocabulary JSON file")
    parser.add_argument("-n", type=int, default=10, help="Number of results to return")
    args = parser.parse_args()

    word_list = load_words_from_json(args.vocab)
    results = vague_search(args.query, word_list, args.n)

    print(f"Top {args.n} results for '{args.query}':")
    for word, distance in results:
        print(f"{word}: {distance}")

if __name__ == "__main__":
    main()