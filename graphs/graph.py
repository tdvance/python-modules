from collections import deque

class Graph:
    """
    Graph() -> new directed graph with no vertices or edges
    """
    def __init__(self):
        self._vertices = dict() #vertex_key -> vertex_data
        self._edges = dict() #edge_key -> edge_data
        self._sources = dict() #edge_key -> vertex_key
        self._targets = dict() #edge_key -> vertex_key
        self._outgoing_edges = dict() #vertex_key -> {edge_key}
        self._incoming_edges = dict() #vertex_key -> {edge_key}
        self._neighbors = dict() #vertex_key -> {vertex_key}
        self._connections = dict() #(vertex_key, vertex_key) -> {edge_key}
        self._aux = dict() #used internally in various algorithms

    def add_vertex(self, key, value=None):
        """Add a new vertex, with an optional value, to the graph.  The key
        must be of a hashable type.  If a vertex of the same key is
        already in the graph and a value is specified, the new value
        will replace the old value.
        """
        if key not in self._vertices:
            self._outgoing_edges[key] = set()
            self._incoming_edges[key] = set()
            self._neighbors[key] = set()
            self._vertices[key] = value
        elif value is not None:
            self._vertices[key] = value

    def add_edge(self, key, source_key, target_key, value=None):
        """Add a new edge, with an optional value, to the graph, connecting
        the specified source vertex key to the specified target vertex
        key.  The keys must be of hashable types.  If the vertices are
        not already in the graph, they will be added with no value.
        If the edge key is already in the graph with the same source
        and target vertex keys and the value is specified, the new
        value will overwrite the old value.  If the edge key is in the
        graph with different source and vetex keys, an exception will
        be raised.
        """
        if key in self._edges:
            if self._sources[key] != source_key:
                raise Exception("Edge %s exists with different endpoints" % key)
            if self._targets[key] != targets_key:
                raise Exception("Edge %s exists with different endpoints" % key)                
            if value is not None:
                self._edges[key] = value
        else:
            self.add_vertex(source_key)
            self.add_vertex(target_key)            
            self._edges[key] = value
            self._sources[key] = source_key
            self._targets[key] = target_key
            self._outgoing_edges[source_key].add(key)
            self._incoming_edges[target_key].add(key)
            self._neighbors[source_key].add(target_key)
            self._neighbors[target_key].add(source_key)
            if not (source_key, target_key) in self._connections:
                self._connections[(source_key, target_key)] = set()
            self._connections[(source_key, target_key)].add(key)

    def remove_edge(self, key):
        """Remove the edge having the specified key, and return the value, if
        any.

        """
        if key in self._edges:
            value = self._edges[key]
            del self._edges[key]
            source_key =  self._sources[key]
            del self._sources[key]
            target_key = self._targets[key]
            del self._targets[key]
            self._outgoing_edges[source_key].remove(key)
            self._incoming_edges[target_key].remove(key)
            self._neighbors[source_key].remove(target_key)
            self._neighbors[target_key].remove(source_key)
            self._connections[(source_key, target_key)].remove(key)
            if not self._connections[(source_key, target_key)]:
                del self._connections[(source_key, target_key)]
            return value
        else:
            return None

    def remove_vertex(self, key):
        """Remove the vertex with the specified key and return the value, if
        any.  Any edges incident with the vertex will be deleted.

        """
        if key in self._vertices:
            edges = set()
            for edge_key in self._outgoing_edges[key]:
                edges.add(edge_key)
            for edge_key in self._incoming_edges[key]:
                edges.add(edge_key)
            for edge_key in edges:
                self.remove_edge(edge_key)
            value = self._vertices[key]
            del self._vertices[key]
            del self._outgoing_edges[key]
            del self._incoming_edges[key]
            neighbors = self._neighbors[key]
            for vertex_key in neighbors:
                self._neighbors[vertex_key].remove(key)
            del self._neighbors[key]
            del edges
            return value
        else:
            return None

    def get_vertex(self, key):
        """Get the value of the vertex having the specified key"""
        return self._vertices[key]

    def is_vertex(self, key):
        """Return True if the key is of a vertex in the graph"""
        return key in self._vertices

    def num_vertices(self):
        """Return the number of vertices in the graph"""
        return len(self._vertices)

    def iter_vertices(self):
        """Generate the vertex keys"""
        for key in self._vertices:
            yield key

    def get_edge(self, key):
        """Get the value of the edge having the specified key"""
        return self._edges[key]

    def is_edge(self, key):
        """Return True if the key is of an edge in the graph"""
        return key in self._edges

    def num_edges(self):
        """Return the number of edges in the graph"""
        return len(self._edges)

    def iter_edges(self):
        """Generate the edge keys"""
        for key in self._edges:
            yield key            
    
    def get_source(self, edge_key):
        """Return the source vertex of the edge key"""
        return self._sources[edge_key]

    def get_target(self, edge_key):
        """Return the target vertex of the edge key"""
        return self._targets[edge_key]

    def iter_outgoing_edges(self, vertex_key):
        """Generate the edge keys coming out of the specified vertex key"""
        for edge_key in self._outgoing_edges[vertex_key]:
            yield edge_key

    def iter_target_vertices(self, vertex_key):
        """Generate the target vertex keys of edges coming out of the
specified vertex key

        """
        for edge_key in self._outgoing_edges[vertex_key]:
            yield self.get_target(edge_key)
            
    def outdegree(self, vertex_key):
        """Return the number of outgoing edges from the specified vertex key"""
        return len(self._outgoing_edges[vertex_key])

    def iter_incoming_edges(self, vertex_key):
        """Generate the edge keys entering the specified vertex key"""
        for edge_key in self._incoming_edges[vertex_key]:
            yield edge_key

    def iter_source_vertices(self, vertex_key):
        """Generate the source vertex keys of edges entering the specified
vertex key

        """
        for edge_key in self._incoming_edges[vertex_key]:
            yield self.get_source(edge_key)
            
    def indegree(self, vertex_key):
        """Return the number of incoming edges to the specified vertex key"""
        return len(self._incoming_edges[vertex_key])            

    def iter_neighbors(self, vertex_key):
        """Generate the vertex keys adjacent to the specified vertex key"""
        for key in self._neighbors[vertex_key]:
            yield key

    def degree(self, vertex_key):
        """Return the number of vertices adjacent to the specified vertex key"""
        return len(self._neighbors[vertex_key])
            
    def iter_connections(self, source_key, target_key):
        if source_key not in self._vertices or target_key not in self._vertices:
            raise KeyError
        if self._connections[(source_key, target_key)]:
            for edge_key in self._connections[(source_key, target_key)]:
                yield edge_key

    def num_connections(self, source_key, target_key):
        """Return the number of edges from the source vertex key to the target
        vertex key

        """
        if source_key not in self._vertices or target_key not in self._vertices:
            raise KeyError
        if self._connections[(source_key, target_key)]:
            return len(self._connections[(source_key, target_key)])
        else:
            return 0
        
    def is_adjacent(self, source_key, target_key):
        """Return true if the specified source vertex key is adjacent to the
        specified target vertex key.

        """
        if source_key not in self._vertices or target_key not in self._vertices:
            raise KeyError
        if (source_key, target_key) in self._connections:
            return True
        return False

    def iter_vertex_values(self):
        """Generate the values of the vertices of the graph"""
        for key in self._vertices:
            yield self._vertices[key]

    def iter_edge_values(self):
        """Generate the values of the edges of the graph"""
        for key in self._edges:
            yield self._edges[key]

    def iter_vertex_value_tuple(self):
        """Generate all vertex key-value pairs from the graph"""
        for key  in self._vertices:
            value = self._vertices[key]
            yield (key, value)
                
    def iter_edge_source_target_value_tuple(self):
        """Generate all edge key-source-target-value quadruples from the graph"""
        for key in self._edges:
            source = self._sources[key]
            target = self._targets[key]
            value = self._edges[key]
            yield (key, source, target, value)
            
    def clear(self):
        """Remove all vertices, edges, and values from the graph"""
        self._vertices.clear()
        self._edges.clear()
        self._sources.clear()
        self._targets.clear()
        self._outgoing_edges.clear()
        self._incoming_edges.clear()
        self._neighbors.clear()
        self._connections.clear()

    def copy(self):
        """Return a shallow copy of the graph"""
        result = Graph()
        result._vertices = self._vertices.copy()
        result._edges = self._edges.copy()
        result._sources = self._sources.copy()
        result._targets = self._targets.copy()
        result._outgoing_edges = self._outgoing_edges.copy()
        result._incoming_edges = self._incoming_edges.copy()
        result._neighbors = self._neighbors.copy( )
        result._connections = self._connections.copy()
        return result

    def __str__(self):
        return "<Graph with %d vertices and %d edges>" %(self.num_vertices(), self.num_edges())

    def __repr__(self):
        return "<Graph with %d vertices and %d edges>" %(self.num_vertices(), self.num_edges())    

    def from_tuple_set_tuple(self, tst):
        """Given graph data in the form (vertices, edges), where vertices is
        an iterable of tuples (vertex_key, vertex_value) and edges is
        an iterable of tuples (edge_key, source_vertex_key,
        target_vertex_key, edge_value), load the data into the current
        graph.  Collisions of edge keys can cause this to fail.  Using
        the clear method on the graph first will prevent this.

        """
        vertices, edges = tst
        for vertex_key, vertex_value in vertices:
            self.add_vertex(vertex_key, vertex_value)
        for edge_key, source_vertex_key, target_vertex_key, edge_value in edges:
            self.add_edge(edge_key, source_vertex_key, target_vertex_key, edge_value)
    
    def to_tuple_set_tuple(self):
        """Return data of the graph, in the form (vertices, edges), where
        vertices is a set of tuples (vertex_key, vertex_value) and
        edges is a set of tuples (edge_key, source_vertex_key,
        target_vertex_key, edge_value).

        """
        return ({t for t in self.iter_vertex_value_tuple()}, {t for t in self.iter_edge_source_target_value_tuple()})

    # basic operations for various graph traversal algorithms
    # from http://www.cs.cornell.edu/courses/cs2112/2012sp/lectures/lec24/lec24-12sp.html
    
    def _tricolor_init(self, *roots):
        self._aux['black'] = set()
        self._aux['gray'] = {x for x in roots}

    def _tricolor_is_white(self, vertex):
        return vertex not in self._aux['black'] and vertex not in self._aux['gray']

    def _tricolor_make_gray(self, vertex):
        assert vertex not in self._aux['black']
        self._aux['gray'].add(vertex)

    def _tricolor_make_black(self, vertex):
        self._aux['black'].add(vertex)
        self._aux['gray'].remove(vertex)
        
    def _tricolor_make_gray_neighbors(self, vertex, op=None):
        for n in self.iter_neighbors(vertex):
            if self._tricolor_is_white(n):
                self._tricolor_make_gray(n)
                if op is not None:
                    op(n)                

    def _tricolor_make_gray_targets(self, vertex, op=None):
        for e in self.iter_outgoing_edges(vertex):
            n = self.get_target(e)
            if self._tricolor_is_white(n):
                self._tricolor_make_gray(n)
                if op is not None:
                    op(n)

    def bfs_undirected(self, *start_vertices):
        """Generate vertices connected to one or more of the start vertices
        in breadth-first order, ignoring direction.

        """
        frontier = deque()  
        for v in start_vertices:
            frontier.append(v)
        self._tricolor_init(*start_vertices)
        while frontier:
            v = frontier.popleft()
            self._tricolor_make_black(v)
            yield v
            self._tricolor_make_gray_neighbors(v, frontier.append)

    def bfs_directed(self, *start_vertices):
        """Generate vertices that are in directed paths starting with one or
        more of the start vertices in breadth-first order, following
        direction.

        """        
        frontier = deque()  
        for v in start_vertices:
            frontier.append(v)
        self._tricolor_init(*start_vertices)
        while frontier:
            v = frontier.popleft()
            self._tricolor_make_black(v)
            yield v
            self._tricolor_make_gray_targets(v, frontier.append) 
            
    def dfs_undirected(self, *start_vertices):
        """Generate vertices connected to one or more of the start vertices
        in depth-first order, ignoring direction.

        """
        frontier = list()  
        for v in start_vertices:
            frontier.append(v)
        self._tricolor_init(*start_vertices)
        while frontier:
            v = frontier.pop()
            self._tricolor_make_black(v)
            yield v
            self._tricolor_make_gray_neighbors(v, frontier.append)

    def dfs_directed(self, *start_vertices):
        """Generate vertices that are in directed paths starting with one or
        more of the start vertices in depth-first order, following
        direction.

        """        
        frontier = list()  
        for v in start_vertices:
            frontier.append(v)
            self._tricolor_init(*start_vertices)
        while frontier:
            v = frontier.pop()
            self._tricolor_make_black(v)
            yield v
            self._tricolor_make_gray_targets(v, frontier.append) 
