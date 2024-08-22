class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

    def __str__(self):
        return (
            f"|{self.type},{self.leaf}|({', '.join(str(child) for child in self.children)})"
            if self.children
            else f"{self.type}({self.leaf})"
        )
