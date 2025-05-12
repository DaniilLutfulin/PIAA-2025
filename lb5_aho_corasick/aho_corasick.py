alphabet = list('ACGTN')

class Node():
    def __init__(self, parent = None):
        self.suff_link = None
        self.term_link = None
        self.term_word = -1
        self.to = dict.fromkeys(alphabet)

    def get_children(self):
        return [(letter, node) for letter, node in self.to.items() if node is not None]

class Trie():
    def __init__(self):
        self.root = Node()
        self.root.suff_link = self.root

    def add_str(self,str, i):
        cur_node = self.root
        for char in str:
            if not cur_node.to[char]:
                cur_node.to[char] = Node(cur_node)
            cur_node = cur_node.to[char]
        cur_node.term_word = i

    def set_sufflink(self, node, parent, char):
        cur_node = parent.suff_link
        while cur_node != self.root and not cur_node.to[char]:
            cur_node = cur_node.suff_link
        next_node = cur_node.to[char]
        if next_node and next_node != node:
            node.suff_link = next_node
        else:
            node.suff_link = self.root

        if node.suff_link.term_word != -1:
            node.term_link = node.suff_link
        else:
            node.term_link = node.suff_link.term_link
    def place_words(self, words):
        for i,word in enumerate(words):
            self.add_str(word, i)
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            for char, child in node.get_children():
                self.set_sufflink(child, node, char)
                queue.append(child)

def count_nodes(node):
    count = 1
    for _, child in node.get_children():
        count += count_nodes(child)
    return count

def find_substrings(text, words, return_count = False):
    trie = Trie()
    answer = []
    trie.place_words(words)
    cur_node = trie.root
    for i in range(len(text)):
        char = text[i]

        while not cur_node.to[char] and cur_node != trie.root:
            cur_node = cur_node.suff_link
        cur_node = cur_node.to[char] or trie.root
        # Поднимаемся по терминальным ссылкам
        temp = cur_node if cur_node.term_word != -1 else cur_node.term_link
        while temp is not None:
            word = temp.term_word
            answer.append((i+2-len(words[word]), word+1))
            temp = temp.term_link

    if return_count:
        return answer, count_nodes(trie.root)
    return answer

def find_intersections(text, words):
    ans = find_substrings(text, words)
    pairs = []
    for i in range(len(ans) - 1):
        if ans[i][0] + len(words[ans[i][1]-1]) > ans[i+1][0]:
            pairs.append((ans[i][1], ans[i+1][1], ans[i][0]))
    return pairs

def count_nodes(node):
    count = 1
    for _, child in node.get_children():
        count += count_nodes(child)
    return count

text = input()
n = int(input())
words = []
for i in range(n):
    words.append(input())

print("Вхождения подстрок:")
substrings, count = find_substrings(text, words, return_count=True)
for x in sorted(substrings):
    print(*x)

print("Пересечения подстрок:")
pairs = find_intersections(text,words)
print(*pairs,sep='\n')

print("Всего вершин в боре:")
print(count)

