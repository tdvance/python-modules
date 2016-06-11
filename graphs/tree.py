import numbers

from graphs.graph import Graph

class Tree:
    """Tree() -> new tree with one node (root) and an optional value and no parent"""

    def __init__(self, value=None):
        """Tree() -> new tree with one node (root) and an optional value and no parent"""       
        self._parent = None
        self._value = value
        self._children = []
        self._index = None #used in the to_graph method

    @property
    def parent(self):
        """Return the parent tree, or None if it is not a subtree of a tree.

        """
        return self._parent

    def find_root(self):
        """Return the root of the tree containing this subtree."""
        t = self
        while t._parent is not None:
            t = t._parent
        return t

    def get_depth(self):
        """Return the number of levels this subtree is from the root"""
        depth = 0
        t = self
        while t._parent is not None:
            depth += 1
            t = t._parent
        return depth

    @property
    def value(self):
        """Return the value of this subtree's top node"""
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of this subtree's top node"""
        self._value = value

    def index(self):
        """Return the index as a child of its parent, if  it is not root"""
        if self._parent is None:
            raise Exception("Tree is root")
        for i in range(len(self._parent)):
            if self == self._parent[i]:
                return i
        assert("Tree structure is corrupt")
        
    def add_child(self, value=None):
        """Create a new child node, appended to the children of the root.
Return the new subtree.

        """
        c = Tree(value)
        self._children.append(c)
        c._parent = self
        return c

    def __setitem__(self, i, tree):
        """replace the subtree rooted at the ith child of this tree with the
specified tree.  This reparents the specified tree and the replaced
subtree.  The tree must be removed as a subtree from any other tree
first.

        """
        if tree._parent is not None:
            raise Exception("Tree still has a parent")
        if self.find_root() == tree:
            raise Exception("Tree being added to itself ")
        c = self[i]
        c._parent = None
        self._children[i] = tree
        tree._parent = self

    def __getitem__(self,  i):
        """Return the subtree rooted at the ith child of this tree"""
        return self._children[i]

    def __delitem__(self, i):
        """Remove the subtree rooted at the ith child of this tree.  This
reparents the removed subtree.

        """
        c = self[i]
        del self._children[i]
        c._parent = None

    def __iter__(self):
        return iter(self._children)
        
    def remove_child(self,  i=None):
        """Remove and return the subtree rooted at the ith (default: last)
        child of this tree.  This reparents the subtree.

        """
        if i is None:
            i = len(self) - 1
        s = self[i]
        del self[i]
        s._parent  = None
        return s
    
    def __len__(self):
        """Return the number of child subtrees of this tree's top node"""
        return len(self._children)

    def clear(self):
        """Clear all children from this tree, leaving just the root.  This
reparents the removed subtrees."""
        for i in range(len(self)):
            self[i]._parent = None
        self._children.clear()

    def copy(self):
        """Return a copy of this tree (with the same values, not copies), but
with no parent"""
        t = Tree(self.value)
        for i in range(len(self)):
            t.insert(0, self[i].copy())
        return t

    def insert(self, index, tree):
        """Insert specified tree as a child subtree before the specified
index.  This reparents the specified tree.  The tree must be removed
as a subtree from any other tree first.

        """
        if tree._parent is not None:
            raise Exception("Tree still has a parent")
        if self.find_root() == tree:
            raise Exception("Tree being added to itself ")
        tree._parent = self
        self._children.insert(index, tree)
     

    def preorder(self):
        """Generate all subtrees of this tree in pre-order"""
        s = []
        current = self
        s.append(current)
        while s:
            current = s.pop()
            if current:
                s.extend(reversed(current))
            yield current   

    def preorder_value_depth(self):
        """Generate all pairs of values and their depths in pre-order"""
        for node in self.preorder():
            yield node.value, node.get_depth()
    
            
    def to_string(self, open_='[', close_=']', sep= ", ", repr_open="Tree(", repr_close=")", elipsis = '...', max_depth=None, repr_style=False):
        """Return a compact function-like string representation, allowing a
        maximum depth and choice of str(tree)-style or
        repr(tree)-style string.

        """
        def maybe_str(s, depth):
            if max_depth is None or depth < max_depth:
                return s
            else:
                return ""

        result = ""
        top_depth = self.get_depth()
        paren_depth = top_depth        
        comma = False
        for value, depth in self.preorder_value_depth():
            while depth < paren_depth:
                result += maybe_str(close_, depth)
                paren_depth -= 1
                comma = True
            if comma:
                result += maybe_str(sep, depth)
            if repr_style:
                s = maybe_str(repr_open + repr(value) + repr_close + open_, depth)
            else:
                s = maybe_str(str(value) + open_, depth)                
            if s:
                result += s
            elif max_depth == depth:
                result += s + elipsis
            comma = False
            paren_depth += 1
        while  paren_depth > top_depth:
            result += maybe_str(close_, depth)
            paren_depth -= 1
        return result
            
    def dir(self, max_depth=15, repr_style=False, elipsis=' ...', indent=4):
        """Return a multiline, readible string representation of this tree,
allowing a maximum depth and setting indentation

        """
        def maybe_str(s, depth):
            if max_depth is None or depth < max_depth:
                return s + '\n'
            elif depth==max_depth:
                return s + elipsis + '\n'
            else:
                return ''
        result = ''
        for value, depth in self.preorder_value_depth():
            indent_str =  " "*(indent*depth)
            if(repr_style):
                result += maybe_str(indent_str+repr(value), depth)
            else:
                result += maybe_str(indent_str+str(value), depth)
        return result

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string(repr_style=True)

    def to_graph(self):
        """
        Create a graph from this tree, vertices pointing toward their parents.
        """
        g = Graph()
        count = 0
        for vertex in self.preorder():
            vertex._index = count
            g.add_vertex(vertex._index, vertex.value)
            if vertex.parent is not None:
                g.add_edge(vertex._index, vertex._index, vertex.parent._index)
            count += 1
        return g
            
            
            
