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
def actionForward(stateActionForward, nodeNumber):
    # at first i check what was the old color and then i change it using this switcher
    global oldColor
    for allColors in stateActionForward.get(str(nodeNumber), []):
        oldColor = allColors
    # oldColor = allColors[0]
    switcher = {
        1: 2,
        2: 3,
        3: 1
    }
    newColor = switcher.get(oldColor)
    # here i change the old color and new color and return the state
    stateActionForward[str(nodeNumber)][0] = newColor


def actionBackward(stateActionBack, nodeNumber):
    # at first i check what was the old color and then i change it using this switcher
    global oldColor
    for allColors in stateActionBack.get(str(nodeNumber), []):
        oldColor = allColors
    switcher = {
        1: 3,
        2: 1,
        3: 2
    }
    newColor = switcher.get(oldColor)
    # here i change the old color and new color and return the state
    stateActionBack[str(nodeNumber)][0] = newColor


def hillClimbingFirstChoise(colorHill, graphHill, nodeNum, firstChance):
    queue = []
    # this is the first value of how much Probability should we consider for simulated annealing
    chance = firstChance
    extendSize = 0
    visitSize = 1
    # here i measure the real size of each algorithm in bytes
    storage = 0
    # this the the value that every time that we used our chance,will increase our chance for not going on chance
    discount = 1.1
    # here I must generate all adjacent states that one situation has
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
        while 1:
            if sys.getsizeof(queue) > storage:
                storage = sys.getsizeof(queue)
            # here i randomly make a new state
            # this random is for picking forward change or backward change in current state, 1 is for forward and
            # 2 is for backward
            rand = random.randint(1, 2)
            # this random is for picking one node to apply changes on
            randNode = random.randint(1, nodeNum)
            # here i set a threshold that if one state was a local minimal,after generating n new states and
            # can't find a better state than our current,so it will print that is local minimal
            if queue.__len__() > 100:
                print("colors : ")
                print(listHill)
                print("score for this colors : " + str(score))
                print("this is local minimal")
                return extendSize, visitSize, storage
            if rand == 1:
                actionForward(colorHill, randNode)
                tempForward = evaluation(colorHill, graphHill)
                visitSize += 1
                listForward = []
                # i used this casting model to avoid conflicting date via call by reference
                for u in colorHill:
                    for y in colorHill.get(u, []):
                        listForward.append(y)
                # finish state
                if tempForward == 0:
                    print("colors : ")
                    print(listForward)
                    print("score for this colors : " + str(tempForward))
                    print("this is the answer")
                    return extendSize, visitSize, storage
                    # undoing the action
                actionBackward(colorHill, randNode)
                # updating the color hill if we find a state that is better than current state
                if score > tempForward:
                    i = 0
                    extendSize += 1
                    for u in colorHill:
                        colorHill[u][0] = listForward[i]
                        i += 1
                    break
                else:
                    # here simulated annealing appears
                    p = random.randint(0, 100)
                    if p > chance:
                        i = 0
                        extendSize += 1
                        for u in colorHill:
                            colorHill[u][0] = listForward[i]
                            i += 1
                        chance = chance * discount
                    # if the random state wasn't better,then i add that to a queue that next time i don't check this
                    # state
                if listForward not in queue:
                    queue.append((listForward, tempForward))
            else:
                actionBackward(colorHill, randNode)
                visitSize += 1
                tempBackward = evaluation(colorHill, graphHill)
                listBackward = []
                # i used this casting model to avoid conflicting date via call by reference
                for u in colorHill:
                    for y in colorHill.get(u, []):
                        listBackward.append(y)
                # finish state
                if tempBackward == 0:
                    print("colors : ")
                    print(listBackward)
                    print("score for this colors : " + str(tempBackward))
                    print("this is the answer")
                    return extendSize, visitSize, storage

                # undoing the action
                actionForward(colorHill, randNode)
                # updating the color hill if we find a state that is better than current state
                if score > tempBackward:
                    i = 0
                    extendSize += 1
                    for u in colorHill:
                        colorHill[u][0] = listBackward[i]
                        i += 1
                    break
                else:
                    # here simulated annealing appears
                    p = random.randint(0, 100)
                    if p > chance:
                        i = 0
                        extendSize += 1
                        for u in colorHill:
                            colorHill[u][0] = listBackward[i]
                            i += 1
                        chance = chance * discount

                    # if the random state wasn't better,then i add that to a queue that next time i don't check this
                    # state
                if listBackward not in queue:
                    queue.append((listBackward, tempBackward))


if __name__ == "__main__":
    numberOfNodes = graph.__len__()
    extend, visit, storage = hillClimbingFirstChoise(color, graph, numberOfNodes, 1)
    print("extended : ", extend, " visited : ", visit, " Storage : ", storage)
