import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N
VP -> V | V NP | V NP PP | V Adv | V PP | V NP PP PP
PP -> P NP
Det -> "a" | "the" | "my"
N -> "holmes" | "companion" | "paint" | "palm" | "pipe" | "day" | "thursday" | "armchair" | "smile" | "word" | "door" | "mess" | "walk"
Adj -> "little" | "moist" | "red" | "dreadful"
V -> "sat" | "lit" | "arrived" | "chuckled" | "smiled" | "said" | "came" | "home"
Adv -> "enigmatical" | "never"
P -> "in" | "on" | "down" | "at"
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)
    words = [word.lower() for word in words]
    words = [word for word in words if any(c.isalpha() for c in word)]

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and not any(subtree.contains(noun_chunk) for noun_chunk in np_chunks):
            np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
