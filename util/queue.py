from .dll import DoublyLinkList


class Queue:
    def __init__(self):
        self.queue = DoublyLinkList()

    def __len__(self):
        return len(self.queue)

    def enqueue(self, value):
        self.queue.add_to_head(value)

    def dequeue(self):
        if not self.queue.head:
            return
        return self.queue.remove_from_tail()
