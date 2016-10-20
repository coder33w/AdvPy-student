import hashlib
import sys

FLAG = 'canihelp'

class Node :
    def __init__ (self, data) :
        self.data = data
        self.left = None
        self.right = None

    def insert (self, node) :
        if node.data == self.data :
            seek = self
            parent = None
            while seek.left != None :
                parent = seek
                seek = seek.left
            self.data = seek.data
            if parent != None :
                parent.left = None
        elif node.data < self.data :
            if self.left == None :
                self.left = node
            else :
                self.left.insert(node)
        elif node.data > self.data :
            if self.right == None :
                self.right = node
            else :
                self.right.insert(node)

class Tree :
    def __init__ (self) :
        self.nodes = None

    def insert (self, data) :
        node = Node(data)
        if self.nodes == None :
            self.nodes = node
        else :
            self.nodes.insert(node)

    def breadth_first (self) :
        result = []
        queue = [self.nodes]
        while len(queue) > 0 :
            node = queue[0]
            queue = queue[1:]
            result.append(node.data)
            if node.left != None :
                queue.append(node.left)
            if node.right != None :
                queue.append(node.right)
        return result

    def debug (self, node, depth=0, DIR=' ') :
        if node == None :
            return
        print DIR, ' ' * depth, node.data
        self.debug(node.left, depth + 2, 'L')
        self.debug(node.right, depth + 2, 'R')

tree = Tree()
chars = sys.argv[1]
for c in chars :
    tree.insert(c)

result = ''.join(tree.breadth_first())

tree.debug(tree.nodes)

print 'result:', result
print 'flag:', FLAG

if result == FLAG :
    print 'pass'
else :
    print 'fail'