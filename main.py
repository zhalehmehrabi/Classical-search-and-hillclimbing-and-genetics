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
numberOfColors = 4
populationSize = 100
# this is the number of selecting parents using tournament selection
tournamentSize = 2
# this is the number that belongs to te cutter of the crossover
cut = 10
# this is mutation rate
mutationRate = 0.02
# this is number of steps that we had to take to get our expected answer
numberOfGenerations = 500

graph = {
    'WAzer': ['kordestan', 'EAzer', 'zanjan'],
    'EAzer': ['WAzer', 'zanjan', 'ardabil'],
    'ardabil': ['zanjan', 'gilan', 'EAzer'],
    'zanjan': ['WAzer', 'EAzer', 'gilan', 'ardabil', 'kordestan'],
    'gilan': ['ardabil', 'zanjan'],
    'kordestan': ['EAzer', 'zanjan'],
    'kermanshah': ['kordestan', 'hamedan', 'lorestan', 'ilam'],
    'hamedan': ['kordestan', 'kermanshah', 'lorestan', 'markazi', 'qazvin', 'zanjan'],
    'qazvin': ['hamedan', 'markazi', 'alborz', 'mazandaran', 'gilan', 'zanjan'],
    'mazandaran': ['gilan', 'qazvin', 'alborz', 'tehran', 'semnan', 'golestan'],
    'alborz': ['qazvin', 'markazi', 'tehran', 'mazandaran'],
    'tehran': ['alborz', 'markazi', 'qom', 'semnan', 'mazandaran'],
    'markazi': ['hamedan', 'lorestan', 'esfahan', 'qom', 'tehran', 'alborz', 'qazvin'],
    'qom': ['markazi', 'esfahan', 'semnan', 'tehran'],
    'lorestan': ['kermanshah', 'ilam', 'khuzestan', 'chaharmahal', 'esfahan', 'markazi', 'hamedan'],
    'ilam': ['kermanshah', 'lorestan', 'khuzestan'],
    'khuzestan': ['ilam', 'lorestan', 'chaharmahal', 'kohgiluye', 'bushehr'],
    'chaharmahal': ['khuzestan', 'kohgiluye', 'esfahan', 'lorestan'],
    'esfahan': ['qom', 'markazi', 'lorestan', 'chaharmahal', 'kohgiluye', 'fars', 'yazd', 'SKhorasan', 'semnan'],
    'semnan': ['mazandaran', 'tehran', 'qom', 'esfahan', 'SKhorasan', 'RKhorasan', 'NKhorasan', 'golestan'],
    'golestan': ['mazandaran', 'semnan', 'NKhorasan'],
    'NKhorasan': ['golestan', 'semnan', 'RKhorasan'],
    'RKhorasan': ['NKhorasan', 'semnan', 'SKhorasan'],
    'SKhorasan': ['RKhorasan', 'semnan', 'esfahan', 'yazd', 'kerman', 'sistan'],
    'yazd': ['esfahan', 'fars', 'kerman', 'SKhorasan'],
    'fars': ['kohgiluye', 'bushehr', 'hormozgan', 'kerman', 'yazd', 'esfahan'],
    'kohgiluye': ['khuzestan', 'bushehr', 'fars', 'esfahan', 'chaharmahal'],
    'bushehr': ['khuzestan', 'kohgiluye', 'fars', 'hormozgan'],
    'hormozgan': ['bushehr', 'fars', 'kerman', 'sistan'],
    'kerman': ['yazd', 'fars', 'hormozgan', 'sistan', 'SKhorasan'],
    'sistan': ['hormozgan', 'kerman', 'SKhorasan']
}
color = {
    'WAzer': [random.randint(1, numberOfColors)],
    'EAzer': [random.randint(1, numberOfColors)],
    'ardabil': [random.randint(1, numberOfColors)],
    'zanjan': [random.randint(1, numberOfColors)],
    'gilan': [random.randint(1, numberOfColors)],
    'kordestan': [random.randint(1, numberOfColors)],
    'kermanshah': [random.randint(1, numberOfColors)],
    'hamedan': [random.randint(1, numberOfColors)],
    'qazvin': [random.randint(1, numberOfColors)],
    'mazandaran': [random.randint(1, numberOfColors)],
    'alborz': [random.randint(1, numberOfColors)],
    'tehran': [random.randint(1, numberOfColors)],
    'markazi': [random.randint(1, numberOfColors)],
    'qom': [random.randint(1, numberOfColors)],
    'lorestan': [random.randint(1, numberOfColors)],
    'ilam': [random.randint(1, numberOfColors)],
    'khuzestan': [random.randint(1, numberOfColors)],
    'chaharmahal': [random.randint(1, numberOfColors)],
    'esfahan': [random.randint(1, numberOfColors)],
    'semnan': [random.randint(1, numberOfColors)],
    'golestan': [random.randint(1, numberOfColors)],
    'NKhorasan': [random.randint(1, numberOfColors)],
    'RKhorasan': [random.randint(1, numberOfColors)],
    'SKhorasan': [random.randint(1, numberOfColors)],
    'yazd': [random.randint(1, numberOfColors)],
    'fars': [random.randint(1, numberOfColors)],
    'kohgiluye': [random.randint(1, numberOfColors)],
    'bushehr': [random.randint(1, numberOfColors)],
    'hormozgan': [random.randint(1, numberOfColors)],
    'kerman': [random.randint(1, numberOfColors)],
    'sistan': [random.randint(1, numberOfColors)]
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
        #print((listTemp, firstScore))
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
    # while choroSomeList:
    for t in range (populationSize):
        for x in range(tournamentSize):
            # here i randomly choose one set of colors
            rand = random.randint(0, choroSomeList.__len__() - 1)
          #  print("rand : " + str(rand))
         #   print(choroSomeList[rand])
            # group.append(choroSomeList.pop(rand)) #########################################################
            group.append(choroSomeList[rand])
        heapSort(group)
        #print("group : ")
        #print(group)
        #print()
        parentList.append(group.pop(-1))
        #print("parents list : ")
        #print(parentList)
        #print()
        group.clear()
    return parentList


if __name__ == "__main__":
    # plt.plot([1, 20, 30, 40], [1, 4, 9, 16])
    # plt.ylabel('some numbers')
    # plt.show()
    minList = []
    maxList = []
    avgList = []
    minScore = 10
    maxScore = 0
    avgScore = 0
    numberOfNodes = graph.__len__()
    population = firstChoromosome(graph, numberOfNodes, color)
    #parents = parentSelection(population)
    #population = newGeneration(parents)
    #print(population.__len__())
    for p in range(1, numberOfGenerations + 1):
        parents = parentSelection(population)
        population = newGeneration(parents)
        for pop in population:
            path, score = pop
            avgScore = avgScore + score
            if score > maxScore:
                maxScore = score
            if score < minScore:
                minScore = score
        avgtemp = avgScore / (p * populationSize)
        minList.append(minScore)
        maxList.append(maxScore)
        avgList.append(avgtemp)
    avgScore = avgScore / (numberOfGenerations * populationSize)
    print("MAX : " + str(maxScore))
    print("MIN : " + str(minScore))
    print("AVG : " + str(avgScore))
    t = np.arange(0., 5., 0.1)

    # red dashes, blue squares and green triangles
    plt.subplot(212)
    plt.plot(minList, minList, 'r--')
    plt.subplot(221)
    plt.plot(maxList, maxList, 'b--')
    plt.subplot(222)
    plt.plot(avgList, avgList, 'g--')
    plt.show()
