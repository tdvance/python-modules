#!/usr/bin/env python3

from graphs.tree import Tree

def check_tree_validity(tree):
    if tree._parent is not None:
        #check that it is a child of its parent
        assert tree == tree._parent[tree.index()]
    #do the same for all subtrees
    for child in tree:
        check_tree_validity(child)


tree = Tree(value="Test Tree")
check_tree_validity(tree)
assert str(tree) == "Test Tree[]"
assert repr(tree) == "Tree('Test Tree')[]"

c1 = tree.add_child("child 1")
c2 = tree.add_child("child 2")
c3 = tree.add_child("child 3")
c4 = tree.add_child("child 4")
check_tree_validity(tree)
assert str(tree) == "Test Tree[child 1[], child 2[], child 3[], child 4[]]"


c11 = c1.add_child("child 1.1")
c12 = c1.add_child("child 1.2")
c13 = c1.add_child("child 1.3")
c14 = c1.add_child("child 1.4")
c21 = c2.add_child("child 2.1")
c22 = c2.add_child("child 2.2")
c23 = c2.add_child("child 2.3")
c41 = c4.add_child("child 4.1")
check_tree_validity(tree)
assert str(tree) == "Test Tree[child 1[child 1.1[], child 1.2[], child 1.3[], child 1.4[]], child 2[child 2.1[], child 2.2[], child 2.3[]], child 3[], child 4[child 4.1[]]]"

assert str(c2) == "child 2[child 2.1[], child 2.2[], child 2.3[]]"
del c2.parent[1]
check_tree_validity(tree)
assert str(tree) == "Test Tree[child 1[child 1.1[], child 1.2[], child 1.3[], child 1.4[]], child 3[], child 4[child 4.1[]]]"

#all nodes are a child of some factor of the node
tree = Tree(1)

for i in range(2, 1000):
    node = tree
    last = node
    while node :
        for child in node:
            if i % child.value == 0:
                node = child
                break
        if last == node:
            break
        last = node
    node.add_child(i)

check_tree_validity(tree)

l = {n.value for n in tree.preorder()}
assert  len(l) == 999

s = str(tree)

assert s.count("[") == s.count("]")
assert s.count("[") == 999

index = 0
count = 0
i=0
for c in s:
    if c == '[':
        index += 1
    elif c == ']':
        index -= 1
    if index==0:
        count += 1
    assert index >= 0
    i += 1
assert index == 0
assert count == 2 #once at the start, once at the end

def check_graph_validity(graph):
    num_vertices = graph.num_vertices()
    num_edges = graph.num_edges()
    vertices = {v for v in graph.iter_vertex_value_tuple()}
    edges = {e for e in graph.iter_edge_source_target_value_tuple()}
    assert(len(vertices) == num_vertices)
    assert(len(edges) ==num_edges)
    for (v, vv) in vertices:
        assert(graph.is_vertex(v))
        assert(graph.get_vertex(v) is vv)
    assert({v for v in graph.iter_vertices()} == {v for (v,vv) in vertices})
    for(e, s, t, v) in edges:
        assert(graph.is_edge(e))
        assert(graph.get_edge(e) is v)
        assert(graph.get_source(e) is s)
        assert(graph.get_target(e) is t)
        assert(graph.is_adjacent(s, t))
    assert({e for e in graph.iter_edges()} == {e for (e, s, t, v) in edges})
    assert(str(graph) == "<Graph with %d vertices and %d edges>" %(num_vertices, num_edges))
    for (v, vv) in vertices:
        o = {e for e in graph.iter_outgoing_edges(v)}
        i =  {e for e in graph.iter_incoming_edges(v)}
        assert(len(o) == graph.outdegree(v))
        assert(len(i) == graph.indegree(v))
        for e in o:
            assert(graph.get_source(e) == v)
        for e in i:
            assert(graph.get_target(e) == v)
        for (ee, s, t, ev) in edges:
            if s == v:
                assert(ee in o)
            if t == v:
                assert(ee in i)     
        a = {vv for vv in graph.iter_neighbors(v)}
        assert(len(a) == graph.degree(v))
        aa = set()
        for e in o:
            aa.add(graph.get_target(e))
        for e in i:
            aa.add(graph.get_source(e))
        assert(a == aa)
    a = dict()
    for (e,s,t,v) in edges:
        if not (s,t) in a:
            a[(s,t)] = set()
        a[(s,t)].add(e)
    aa = dict()
    for (s,vs) in vertices:
        for (t,vt) in vertices:
            if graph.is_adjacent(s,t):
                assert((s,t) in a)
                aa[(s,t)] = set()
                for e in graph.iter_connections(s,t):
                    aa[(s,t)].add(e)
            if not graph.is_adjacent(s,t):
                assert((s,t) not in a)
    assert(aa==a)


graph = tree.to_graph()
check_graph_validity(graph)

assert(graph.num_vertices() == 999)
assert(graph.num_edges() == 998)
