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
price = {
    'Oradea': [71, 151],
    'zeriland': [71, 75],
    'Arad': [75, 140, 118],
    'sibiu': [151, 140, 99, 80],
    'fagaras': [99, 211],
    'Timisoara': [118, 111],
    'Rimnicu': [80, 97, 146],
    'Logoj': [111, 70],
    'Pitesti': [97, 138, 101],
    'Mehadia': [70, 75],
    'Dobreta': [75, 120],
    'Craiova': [120, 146, 138],
    'Bucharest': [211, 101, 90, 85],
    'Giurgiu': [90],
    'Urziceni': [85, 98, 142],
    'Hirsova': [98, 86],
    'Eforie': [86],
    'Vaslui': [142, 92],
    'Lasi': [92, 87],
    'Neamt': [87]
}


# i used the heap sort that was here https://www.geeksforgeeks.org/heap-sort/ but i changed it much
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n:
        pathi, costi = arr[i]
        pathl, costl = arr[l]
        if costi < costl:
            largest = l
    # See if right child of root exists and is
    # greater than root
    if r < n:
        pathLarge, costLarge = arr[largest]
        pathr, costr = arr[r]
        if costLarge < costr:
            largest = r

        # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)

    # The main function to sort an array of given size


def heapSort(arr):
    n = len(arr)
    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(arr, n, i)

        # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)


def uniformCostSearchTree(graph, price, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append(([start], 0))
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0
    while queue:
        # get the first path from the queue
        heapSort(queue)
        path, cost = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        extendSize += 1
        if sys.getsizeof(queue) > storage:
            storage = sys.getsizeof(queue)
            # path found
        if node == end:
            return path, extendSize, visitSize, cost, storage
        # I use this to go forward in price list
        i = 0
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            costFullNode = price.get(node, [])
            costNode = costFullNode[i]
            i += 1
            visitSize += 1
            newCost = cost + costNode
            new_path = list(path)
            new_path.append(adjacent)
            queue.append((new_path, newCost))


def uniformCostSearchGraph(graph, price, start, end):
    # maintain a queue of paths
    queue = []
    # make close list for check if one node was visited before or not and push the root
    closeList = []
    # push the first path into the queue
    queue.append(([start], 0))
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0
    while queue:
        # get the first path from the queue
        heapSort(queue)
        path, cost = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if sys.getsizeof(queue) + sys.getsizeof(closeList) > storage:
            storage = sys.getsizeof(queue) + sys.getsizeof(closeList)
        if node in closeList:
            continue
        extendSize += 1
        closeList.append(node)
        # path found
        if node == end:
            return path, extendSize, visitSize, cost, storage
        # I use this to go forward in price list
        i = 0
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            if adjacent in closeList:
                i += 1
                continue
            costFullNode = price.get(node, [])
            costNode = costFullNode[i]
            i += 1
            visitSize += 1
            newCost = cost + costNode
            new_path = list(path)
            new_path.append(adjacent)
            queue.append((new_path, newCost))


if __name__ == "__main__":
    path, extend, visit, cost, storage = uniformCostSearchGraph(graph, price, 'Arad', 'Bucharest')
    print("Path : ", path, " Cost : ", cost, " Extended : ", extend, " Visited : ", visit, " Storage : ",
          storage)
