alphabet = list('ACGTN')


class Node():
    def __init__(self, parent=None):
        self.parent = parent
        self.to = dict.fromkeys(alphabet)
        self.suff_link = None
        self.term_link = None
        self.terms = [] # (part_idx, offset_in_pattern)

    def get_children(self):
        return [(char, node) for char, node in self.to.items() if node is not None]


class Trie():
    def __init__(self):
        self.root = Node()
        self.root.suff_link = self.root

    def add_str(self, s, part_idx):
        cur = self.root
        for char in s:
            if not cur.to[char]:
                cur.to[char] = Node(cur)
            cur = cur.to[char]
        cur.terms.append(part_idx)

    def set_sufflink(self, node, parent, char):
        cur = parent.suff_link
        while cur is not self.root and not cur.to[char]:
            cur = cur.suff_link
        if cur.to[char] and cur.to[char] is not node:
            node.suff_link = cur.to[char]
        else:
            node.suff_link = self.root

        if node.suff_link.terms:
            node.term_link = node.suff_link
        else:
            node.term_link = node.suff_link.term_link

    def build(self, parts):
        # parts = [(substring, offset), ...]
        for i, (substr, offset) in enumerate(parts):
            self.add_str(substr, i)
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            for char, child in node.get_children():
                self.set_sufflink(child, node, char)
                queue.append(child)

def split_pattern(P, wild_card):
    parts = []
    pos = 0
    for part in P.split(wild_card):
        if part:
            parts.append((part, pos))
        pos += len(part) + 1
    return parts


def find_wildcard(text, pattern, joker='?'):
    parts = split_pattern(pattern, joker) # (part,pos)
    t = Trie()
    t.build(parts)

    matches = {}
    node = t.root

    for i, c in enumerate(text):
        while node is not t.root and not node.to[c]:
            node = node.suff_link
        node = node.to[c] or t.root
        temp = node
        while temp:
            for part_idx in temp.terms:
                substr, offset = parts[part_idx]
                start = (i - len(substr) + 1) - offset
                if 0 <= start <= len(text) - len(pattern):
                    matches.setdefault(start, set()).add(part_idx)
            temp = temp.term_link
    return [pos + 1 for pos, s in matches.items() if len(s) == len(parts)]

T = input().strip()
P = input().strip()
wild_card = input()
for pos in find_wildcard(T, P,wild_card):
    print(pos)
