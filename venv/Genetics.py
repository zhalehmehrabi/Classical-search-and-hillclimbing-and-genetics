import numpy as np
import random
import copy
import matplotlib.pyplot as plt

global numberOfColors
global populationSize
global tournamentSize
global cut
global mutationRate
global numberOfNodes
global numberOfGenerations
# you have to set number of colors and population size here
numberOfColors = 3
populationSize = 1000
# this is the number of selecting parents using tournament selection
tournamentSize = 2
# this is the number that belongs to te cutter of the crossover
cut = 5
# this is mutation rate
mutationRate = 0.1
# this is number of steps that we had to take to get our expected answer
numberOfGenerations = 500

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


# this is the function that validates the state that you give to it
# state is an array that looks like your graph, the graph is my model of the all adjacent nodes
def evaluation(colorVal, graphVal):
    # this is the total number edges * 2
    count = 0
    # this is the total number of edges that connect vertices which have not same colors
    notConflict = 0
    # here is the for that visits all nodes and counts the conflict number between all adjacent nodes
    for node in graphVal:
        for adjacent in graphVal.get(node, []):
            # here i will find the color of each node and each adjacent
            colorAdjacent = colorVal.get(adjacent, [])
            colorNode = colorVal.get(node, [])
            count += 1
            if colorNode[0] != colorAdjacent[0]:
                notConflict += 1
    return notConflict * 2 / count


# here we generate the first population
def firstChoromosome(firstGraph, firstGraphSize, colorFirst):
    list = []
    for x in range(populationSize):
        dicTemp = copy.deepcopy(colorFirst)
        listTemp = []
        for u in range(firstGraphSize):
            listTemp.append(random.randint(1, numberOfColors))
        i = 0
        for u in dicTemp:
            dicTemp[u][0] = listTemp[i]
            i += 1
        firstScore = evaluation(dicTemp, firstGraph)
        list.append((dicTemp, firstScore))
        listTemp.clear()
    return list


def crossOver(firstPopulation, first, second, child):
    father, fatherScore = firstPopulation.__getitem__(first)
    mother, motherScore = firstPopulation.__getitem__(second)
    i = 0
    tmpChild = []
    dicTemp = copy.deepcopy(color)
    # here i make a child using a simple change in father(i take first "cut" number of mother
    for x in mother:
        if i == cut:
            break
        i += 1
        for y in mother.get(x, []):
            tmpChild.append(y)
    i = 0
    for x in father:
        for y in father.get(x, []):
            if i < cut:
                i += 1
                continue
            tmpChild.append(y)
    i = 0
    for u in dicTemp:
        dicTemp[u][0] = tmpChild[i]
        i += 1
    score = evaluation(dicTemp, graph)
    child.append((dicTemp, score))


def mutation(noneMutatedPopulation):
    # this is the number of mutated genomes
    mutatedGenomes = noneMutatedPopulation.__len__() * numberOfNodes * mutationRate
    for x in range(int(mutatedGenomes)):
        member = random.randint(0, noneMutatedPopulation.__len__() - 1)
        genome = random.randint(1, numberOfNodes)
        path, score = noneMutatedPopulation[member]
        for mufind in graph:
            if genome == 0:
                break
            genome -= 1
        # here mutation occurs
        last = path[mufind][0]
        new = random.randint(1, numberOfColors)
        while last == new:
            new = random.randint(1, numberOfColors)
        path[mufind][0] = new
        score = evaluation(path, graph)
        noneMutatedPopulation[member] = path, score


def newGeneration(lastPopulation):
    child = []
    for i in range(lastPopulation.__len__()):
        x = random.randint(0, lastPopulation.__len__() - 1)
        y = random.randint(0, lastPopulation.__len__() - 1)
        crossOver(lastPopulation, x, y, child)
    mutation(child)
    return child


# here i cluster the population in groups of tournament size
def parentSelection(choroSomeList):
    parentList = []
    group = []
    for t in range(populationSize):
        for x in range(tournamentSize):
            # here i randomly choose one set of colors
            rand = random.randint(0, choroSomeList.__len__() - 1)
            group.append(choroSomeList[rand])
        heapSort(group)
        parentList.append(group.pop(-1))
        group.clear()
    return parentList


if __name__ == "__main__":
    minList = []
    maxList = []
    avgList = []
    minScore = 10
    minMain = 10
    maxMain = 0
    maxScore = 0
    avgScore = 0
    numberOfNodes = graph.__len__()
    population = firstChoromosome(graph, numberOfNodes, color)
    for p in range(1, numberOfGenerations + 1):
        parents = parentSelection(population)
        population = newGeneration(parents)
        minScore = 10
        maxScore = 0
        for pop in population:
            path, score = pop
            avgScore = avgScore + score
            if score > maxScore:
                maxScore = score
            if score < minScore:
                minScore = score
            if score < minMain:
                minMain = score
            if score > maxMain:
                maxMain = score
        avgtemp = avgScore / (p * populationSize)
        minList.append(minScore)
        maxList.append(maxScore)
        avgList.append(avgtemp)
    avgScore = avgScore / (numberOfGenerations * populationSize)
    print("MAX : " + str(maxMain))
    print("MIN : " + str(minMain))
    print("AVG : " + str(avgScore))
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].scatter(minList, minList)
    axarr[0, 0].set_title('Min')
    axarr[0, 1].scatter(maxList, maxList)
    axarr[0, 1].set_title('Max')
    axarr[1, 0].scatter(avgList, avgList)
    axarr[1, 0].set_title('Avg')
    plt.show()
