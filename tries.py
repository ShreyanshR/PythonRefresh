from unittest import TestResult


class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        curr = self.root

        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            
            curr = curr.children[c]

        curr.word = True

    def get_all_words(self) -> list[str]:
        """Return all words inserted into the trie."""
        out = []

        def dfs(node: TrieNode, prefix: str) -> None:
            if node.word:
                out.append(prefix)
            for c, child in node.children.items():
                dfs(child, prefix + c)

        dfs(self.root, "")
        return out

    def print_structure(self, node: TrieNode | None = None, prefix: str = "", indent: int = 0) -> None:
        """Print trie structure so you can see repeated chars (e.g. 'd' in 'daddy')."""
        if node is None:
            node = self.root
        for c, child in node.children.items():
            end = " [WORD]" if child.word else ""
            print("  " * indent + f"'{c}'{end} -> children: {list(child.children.keys())}")
            self.print_structure(child, prefix + c, indent + 1)


if __name__ == "__main__":
    S = Trie()

    S.insert("daddy")
    S.insert("dappy")
    print("All inserted words:", S.get_all_words())
    print("\nTrie structure (see how repeated 'd' appears in different nodes):")
    S.print_structure()