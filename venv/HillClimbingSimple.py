import random
import sys
global numberOfColors
# you have to set number of colors here
numberOfColors = 3

graph = {
    '1': ['10', '11', '3', '4'],
    '2': ['5', '3', '7', '11'],
    '3': ['1', '2', '6'],
    '4': ['1', '6', '5'],
    '5': ['2', '4', '10', '8'],
    '6': ['3', '4', '7', '8', '9'],
    '7': ['2', '6', '10'],
    '8': ['5', '6', '11'],
    '9': ['6', '10', '11'],
    '10': ['1', '5', '7', '9'],
    '11': ['1', '2', '8', '9']
}
color = {
    '1': [random.randint(1, numberOfColors)],
    '2': [random.randint(1, numberOfColors)],
    '3': [random.randint(1, numberOfColors)],
    '4': [random.randint(1, numberOfColors)],
    '5': [random.randint(1, numberOfColors)],
    '6': [random.randint(1, numberOfColors)],
    '7': [random.randint(1, numberOfColors)],
    '8': [random.randint(1, numberOfColors)],
    '9': [random.randint(1, numberOfColors)],
    '10': [random.randint(1, numberOfColors)],
    '11': [random.randint(1, numberOfColors)]
}


# this is the function that validates the state that you give to it
# state is an array that looks like your graph, the graph is my model of the all adjacent nodes
def evaluation(colorVal, graphVal):
    # this is the conflict number
    count = 0
    # here is the for that visits all nodes and counts the conflict number between all adjacent nodes
    for node in graphVal:
        for adjacent in graphVal.get(node, []):
            # here i will find the color of each node and each adjacent
            colorAdjacent = colorVal.get(adjacent, [])
            colorNode = colorVal.get(node, [])
            if colorNode[0] == colorAdjacent[0]:
                count += 1
    return count


# this function simply changes the state and makes new state
def actionForward(stateAction, nodeNumber):
    # at first i check what was the old color and then i change it using this switcher
    global oldColor

    for allColors in stateAction.get(str(nodeNumber), []):
        oldColor = allColors
    # oldColor = allColors[0]
    switcher = {
        1: 2,
        2: 3,
        3: 1
    }
    newColor = switcher.get(oldColor)
    # here i change the old color and new color and return the state
    stateAction[str(nodeNumber)][0] = newColor


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


def actionBackward(stateAction, nodeNumber):
    # at first i check what was the old color and then i change it using this switcher
    global oldColor

    for allColors in stateAction.get(str(nodeNumber), []):
        oldColor = allColors
    # oldColor = allColors[0]
    switcher = {
        1: 3,
        2: 1,
        3: 2
    }
    newColor = switcher.get(oldColor)
    # here i change the old color and new color and return the state
    stateAction[str(nodeNumber)][0] = newColor


def hillClimbingSimple(colorHill, graphHill, nodeNum):
    queue = []
    # here i measure the real size of each algorithm in bytes
    storage = 0
    # here I must generate all adjacent states that one situation has
    # in this kind of problems (graph coloring) you can compute that for each state how many adjacent you have
    extendeSize = 0
    visitSize = 1
    while 1:
        # before each step starts, we have to add the starting state and it's score to queue
        # that is the score of starting state
        score = evaluation(colorHill, graphHill)
        # first i add the starting state in the queue
        listHill = []
        # i used this casting model to avoid conflicting date via call by reference
        for u in colorHill:
            for y in colorHill.get(u, []):
                listHill.append(y)
        queue.append((listHill, score))
        for x in range(1, nodeNum + 1):
            listHill = []
            for u in colorHill:
                for y in colorHill.get(u, []):
                    listHill.append(y)
            actionForward(colorHill, x)
            visitSize += 1
            tempForward = evaluation(colorHill, graphHill)
            listForward = []
            # i used this casting model to avoid conflicting date via call by reference
            for u in colorHill:
                for y in colorHill.get(u, []):
                    listForward.append(y)
            queue.append((listForward, tempForward))
            # i need this for finishing if
            if score > tempForward:
                score = tempForward
            # the first will undo the action forward of the line 138
            actionBackward(colorHill, x)
            # the second on is the main backward action
            actionBackward(colorHill, x)
            visitSize += 1
            tempBackward = evaluation(colorHill, graphHill)
            listBackward = []
            # i used this casting model to avoid conflicting date via call by reference
            for u in colorHill:
                for y in colorHill.get(u, []):
                    listBackward.append(y)
            queue.append((listBackward, tempBackward))
            if score > tempBackward:
                score = tempBackward
            # undoing last backward
            actionForward(colorHill, x)
        if sys.getsizeof(queue) > storage:
            storage = sys.getsizeof(queue)
        # now we find the best move inside of all action that we could take using a heap sort
        heapSort(queue)
        bestColor, bestScore = queue.pop(0)
        extendeSize += 1
        scoreHill = evaluation(colorHill, graphHill)
        # if we can not find a better adjacent,we find one answer,it can be local maximal
        if bestColor == listHill or (((listHill, scoreHill) in queue) and scoreHill == bestScore):
            print("colors : ")
            print(bestColor)
            print("score for this colors : " + str(bestScore))
            if bestScore == 0:
                print("this is the answer")
            else:
                print("this is local minimal")
            return extendeSize, visitSize, storage
        else:
            # we have to clear the queue all states that were generated in last step get dumped
            queue.clear()
            # here i update the old colors with the best state of colors that i have found a little bit earlier
            i = 0
            for u in colorHill:
                colorHill[u][0] = bestColor[i]
                i += 1


if __name__ == "__main__":
    numberOfNodes = graph.__len__()
    extend, visit, storage = hillClimbingSimple(color, graph, numberOfNodes)
    print("extended : ", extend, " visited : ", visit, " Storage : ", storage)
