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


def dfsTreeIterativeDeepening(graph, start, end):
    # initialize the first value of depth
    depth = 1
    # initialize the visited number of nodes and extended number on nodes
    visitSize = 1
    extendSize = 0
    # here i measure the real size of each algorithm in bytes
    storage = 0
    while 1:
        # maintain a queue of paths
        queue = []
        # push the first path into the queue
        queue.append([start])
        extendSize += 1
        while queue:
            # get the first path from the queue
            path = queue.pop(queue.__len__() - 1)
            # get the last node from the path
            node = path[-1]
            if sys.getsizeof(queue) > storage:
                storage = sys.getsizeof(queue)
            # path found
            extendSize += 1
            if node == end:
                return path, extendSize, visitSize, storage
            # enumerate all adjacent nodes, construct a new path and push it into the queue if the search doesn't
            # reach the depth
            for adjacent in graph.get(node, []):
                # this line checks that if the depth of the search reached to restriction or not
                if path.__len__() > depth:
                    break
                visitSize += 1
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
        depth += 1


def dfsGraphIterativeDeepening(graph, start, end):
    # initialize the visited number of nodes and extended number on nodes and depth
    depth = 1
    visitSize = 1
    extendSize = 0
    # here i measure the real size of each algorithm in bytes
    storage = 0
    while 1:
        # maintain a queue of paths
        queue = []
        # make close list for check if one node was visited before or not and push the root
        closeList = []
        extendSize += 1
        # push the first path into the queue
        queue.append([start])
        while queue:
            # get the first path from the queue
            path = queue.pop(queue.__len__() - 1)
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
                # this line checks that if the depth of the search reached to restriction or not
                if path.__len__() > depth:
                    break
                if adjacent in closeList:  # checks if one node is visited before or not
                    continue
                visitSize += 1
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
        depth += 1


if __name__ == "__main__":
    path, extend, visit, storage = dfsGraphIterativeDeepening(graph, 'Arad', 'Bucharest')
    print("Path : ", path, " Cost : ", path.__len__() - 1, " Extended : ", extend, " Visited : ", visit, " Storage : ",
          storage)
