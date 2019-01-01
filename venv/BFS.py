import sys
graph = {
    'Oradea': ['zeriland', 'sibiu'],
    'zeriland': ['Oradea', 'Arad'],
    'Arad': ['zeriland', 'sibiu', 'Timisoara'],
    'sibiu': ['Oradea', 'Arad', 'fagaras', 'Rimnicu'],
    'fagaras': ['sibiu', 'Bucharest'],
    'Timisoara': ['Arad', 'Logoj'],
    'Rimnicu': ['sibiu', 'Pitesti', 'Craiova'],
    'Logoj': ['Timisoara', 'Mehadia'],
    'Pitesti': ['Rimnicu', 'Craiova', 'Bucharest'],
    'Mehadia': ['Logoj', 'Dobreta'],
    'Dobreta': ['Mehadia', 'Craiova'],
    'Craiova': ['Dobreta', 'Rimnicu', 'Pitesti'],
    'Bucharest': ['fagaras', 'Pitesti', 'Giurgiu', 'Urziceni'],
    'Giurgiu': ['Bucharest'],
    'Urziceni': ['Bucharest', 'Hirsova', 'Vaslui'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Eforie': ['Hirsova'],
    'Vaslui': ['Urziceni', 'Lasi'],
    'Lasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Lasi']
}


def bfsTree(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        extendSize += 1
        if sys.getsizeof(queue) > storage:
            storage = sys.getsizeof(queue)
        if node == end:
            return path, extendSize, visitSize, storage
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            visitSize += 1
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def bfsGraph(graph, start, end):
    # maintain a queue of paths
    queue = []
    # make close list for check if one node was visited before or not and push the root
    closeList = []
    # push the first path into the queue
    queue.append([start])
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if sys.getsizeof(queue) + sys.getsizeof(closeList) > storage:
            storage = sys.getsizeof(queue) + sys.getsizeof(closeList)
        # checks if one node is visited before or not
        if node in closeList:
            continue
        closeList.append(node)
        extendSize += 1
        # path found
        if node == end:
            return path, extendSize, visitSize, storage
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            if adjacent in closeList:
                continue
            visitSize += 1
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


if __name__ == "__main__":
    path, extend, visit, storage = bfsGraph(graph, 'Arad', 'Bucharest')
    print("Path : ", path, " Cost : ", path.__len__() - 1, " Extended : ", extend, " Visited : ", visit, " Storage : ",
          storage)
