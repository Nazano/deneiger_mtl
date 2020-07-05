import networkx as nx

def find_eulerian_path(G):
    from operator import itemgetter
    if G.is_directed() and not nx.is_weakly_connected(G):
        raise nx.NetworkXError("G is not connected")
    if not G.is_directed() and not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")
    if nx.is_eulerian(G):
        x = nx.eulerian_circuit(G)
        for i in x:
            return i
    else:
        g = G.__class__(G)
        check_odd = []
        directed = False
        
        if g.is_directed():
            degree = g.in_degree
            out_degree = g.out_degree
            edges = g.in_edges()
            get_vertex = itemgetter(0)
            directed = True
        else:
            degree = g.degree
            edges = g.in_edges()
            get_vertex = itemgetter(1)
        for vertex in g.nodes():
            deg = degree(vertex)
            if directed:
                outdeg = out_degree(vertex)
                if deg != outdeg:
                    if len(check_odd) > 2:
                        raise nx.NetworkXError("G doesn't have Euler Path")
                    else:
                        check_odd.append(vertex)
            else:
                if deg % 2 != 0:
                    if len(check_odd) > 2:
                        raise nx.NetworkXError("G doesn't have Euler Path")
                    else:
                        check_odd.append(vertex)
        if directed:
            def verify_odd_cond(g, check_odd):
                first = check_odd[0]
                second = check_odd[1]
                if (g.out_degree(first) == g.in_degree(first) + 1 and 
                        g.in_degree(second) == g.out_degree(second) + 1):
                    return second
                elif (g.out_degree(second) == g.in_degree(second) + 1
                     and g.in_degree(first) == g.out_degree(first) + 1):
                    return first
                else:
                    return None
            start = verify_odd_cond(g, check_odd)
        else:
            start = check_odd[0]
        if not start:
            return nx.NetworkXError("G doesn't have Euler Path")
        
        vertex_stack = [start]
        last_vertex = None
        
        while vertex_stack:
            current_vertex = vertex_stack[-1]
            if degree(current_vertex) == 0:
                if last_vertex is not None:
                    return (last, vertex, current_vertex)
                last_verted = current_vertex
                vertex_stack.pop()
            else:
                random_edge = next(edges(current_vertex))
                vertex_stack.append(get_vertex(random_edge))
                g.remove(*random_edge)
    
def solve(num_vertices, edge_list):
    G = nx.DiGraph()
    for u, v, w in edge_list:
        G.add_edge(u,v,weight=w)
    print(G.edges)
    return find_eulerian_path(G)

edges = [(1, 2, 4), (1, 3, 3), (4, 3, 2), (5, 4, 4), (3, 5, 2)]

s = solve(5,edges)
print(s)


