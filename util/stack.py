from .dll import DoublyLinkList


class Stack:
    def __init__(self):
        self.stack = DoublyLinkList()

    def __len__(self):
        return len(self.stack)

    def push(self, value):
        self.stack.add_to_head(value)

    def pop(self):
        if not self.stack.head:
            return
        return self.stack.remove_from_head()
