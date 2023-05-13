from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    shortest_paths = {vertex: (float('inf'), float('inf')) for vertex in graph}
    shortest_paths[source] = (0, 0)
    def compare_paths(path1, path2):
        weight1, edges1 = path1
        weight2, edges2 = path2
        if weight1 < weight2:
            return -1
        elif weight1 > weight2:
            return 1
        elif edges1 < edges2:
            return -1
        elif edges1 > edges2:
            return 1
        else:
            return 0
    queue = [(0, 0, source)]
    while queue:
        weight, edges, current_node = heappop(queue)
        if compare_paths((weight, edges), shortest_paths[current_node]) > 0:
            continue
        for neighbor, edge_weight in graph[current_node]:
            new_weight = weight + edge_weight
            new_edges = edges + 1
            if compare_paths((new_weight, new_edges), shortest_paths[neighbor]) < 0:
                shortest_paths[neighbor] = (new_weight, new_edges)
                heappush(queue, (new_weight, new_edges, neighbor))

    return shortest_paths
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    parents = {vertex: None for vertex in graph}
    parents[source] = None
    queue = deque([source])
    while queue:
        current_node = queue.popleft()
        for neighbor in graph[current_node]:
            if parents[neighbor] is None:
                parents[neighbor] = current_node
                queue.append(neighbor)

    return parents

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    path = []
    current_node = destination
    while current_node is not None:
        path.append(current_node)
        current_node = parents[current_node]
    path.reverse()
    path_string = "".join(path[:-1])
    return path_string

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
