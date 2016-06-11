#!/usr/bin/env python3

from graphs.graph import Graph


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
    

                
g = Graph()
assert(str(g) == "<Graph with %d vertices and %d edges>" %(0, 0))
check_graph_validity(g)
g.add_vertex('spam')
check_graph_validity(g)
g.add_edge('E1,2', 1, 2)
check_graph_validity(g)
assert(str(g) == "<Graph with %d vertices and %d edges>" %(3, 1))
check_graph_validity(g)
g.remove_vertex(1)
check_graph_validity(g)
g.clear()
check_graph_validity(g)


g.add_vertex("spam")
g.add_vertex("eggs")

for i in range(0,4):
    for j in range(0,4):
        if i<j:
            g.add_edge(str(i)+","+str(j), i, j, i+j)

for i in range(4,8):
    for j in range(4,8):
        if i<j:
            g.add_edge(str(i)+","+str(j), i, j, i+j)            

g.add_edge("bridge", 0, 4)

check_graph_validity(g)
assert(str(g) == "<Graph with %d vertices and %d edges>" %(10, 13))

g.remove_vertex("eggs")
g.remove_edge("bridge")
g.remove_vertex(5)
check_graph_validity(g)
assert(str(g) == "<Graph with %d vertices and %d edges>" %(8, 9))
g = g.copy()
check_graph_validity(g)
assert(str(g) == "<Graph with %d vertices and %d edges>" %(8, 9))
gg = g.to_tuple_set_tuple()
hh = ({(6, None), ('spam', None), (4, None), (1, None), (7, None), (0, None), (3, None), (2, None)}, {('4,6', 4, 6, 10), ('1,2', 1, 2, 3), ('0,3', 0, 3, 3), ('4,7', 4, 7, 11), ('0,1', 0, 1, 1), ('0,2', 0, 2, 2), ('6,7', 6, 7, 13), ('1,3', 1, 3, 4), ('2,3', 2, 3, 5)})
assert(gg==hh)

for i in range(5, 20):
    g.add_vertex(i, i)

for  i in range(17, 27):
    for j in range (6, 13):
        g.add_edge(str(i)+"->"+str(j), i, j)

for i in range (15, 19):
    for j in range (7, 11):
        g.remove_edge(str(i)+"->"+str(j))

for i in range(18, 22):
    g.remove_vertex(i)

check_graph_validity(g)

g = Graph()

for i in range(2, 1000):
    j = i-1
    g.add_edge(str(j) + "|" + str(i), i, j)

last_v=1000
for v in g.dfs_directed(999):
    assert v < last_v
    last_v = v


g = Graph()
g.add_edge("ab", "a", "b")
g.add_edge("ac", "a", "c")
g.add_edge("ad", "a", "d")
g.add_edge("be", "b", "e")
g.add_edge("cf", "c", "f")
g.add_edge("dg", "d", "g")

s = [x for x in g.bfs_directed("a")]
assert s[0] == 'a'
assert set(s[1:4]) == {'b', 'c', 'd'}
assert set(s[4:7]) == {'e', 'f', 'g'}
s = [x for x in g.dfs_directed("a")]
assert s[0] == 'a'
assert {s[1], s[3], s[5]} == {'b', 'c', 'd'}
assert {s[2], s[4], s[6]} == {'e', 'f', 'g'}
