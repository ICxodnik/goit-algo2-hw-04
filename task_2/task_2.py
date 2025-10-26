from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string")

        count = 0

        def dfs(node, path):
            nonlocal count
            if hasattr(node, "value") and node.value is not None:
                if path.endswith(pattern):
                    count += 1
            for char, child in getattr(node, "children", {}).items():
                dfs(child, path + char)

        dfs(self.root, "")
        return count

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise ValueError("Prefix must be a string")
        node = self.root
        for char in prefix:
            if char not in getattr(node, "children", {}):
                return False
            node = node.children[char]
        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat

print("Тести пройдено")