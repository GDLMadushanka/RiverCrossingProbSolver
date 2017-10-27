import networkx as nx
import pylab as plt
import itertools

goalNodeNo = 0
previousNodeNo = 0
currentNodeNo = 1
currentLayerNo = 1
g = nx.DiGraph()
boatCapacity = 2
goalReached = False

# restrikted states of river banks and boat
restricktedRiverbank = []
restricktedBoat = []

bank1Status = []
bank2Status = []

driverArr = []
rolesArr = []
nonDriverArr = []


# validate the combination on riverbank
def validateRiverbank(arr):
    for i in restricktedRiverbank:
        if sorted(i) == sorted(arr):
            return False
    return True


# validate the combination on boat
def validateBoat(arr):
    for i in restricktedBoat:
        if sorted(i) == sorted(arr):
            return False
    return True


# generating all possible combinations and remove lists without drivers
def generatePermutations(arr):
    validPermutations = []
    for j in range(boatCapacity):
        temp = itertools.combinations(arr, j + 1)
        for i in temp:
            tem = set(i).intersection(driverArr)
            if len(tem) > 0:
                validPermutations.append(list(i))
    return validPermutations


# validate generated permutations
#   remove combinations without any driver
#   remove combinations that leave starting riverbank incorrect
#   remove combinations that makes destination riverbank incorrect
def validatePermutations(arr, l):
    global bank2Status
    global bank1Status
    arr1 = arr[:]
    for i in arr1:
        if not validateBoat(i):
            arr.remove(i)
            continue
        if l % 2 == 0:
            tempBank1 = list(set(bank1Status) - set(i))
            if not validateRiverbank(tempBank1):
                arr.remove(i)
                continue
            tempBank2 = bank2Status + i
            if not validateRiverbank(tempBank2):
                arr.remove(i)
        else:
            tempBank1 = bank1Status + i
            if not validateRiverbank(tempBank1):
                arr.remove(i)
                continue
            tempBank2 = list(set(bank2Status) - set(i))
            if not validateRiverbank(tempBank2):
                arr.remove(i)

    return arr


# add node to chart if not already exists
def addNodeIfNotExist(arrBank1, arrBank2, l):
    global g
    global goalReached
    global currentNodeNo
    global previousNodeNo
    global goalNodeNo
    global rolesArr
    ppp = filter(lambda (k, v): set(v['bank1']) == set(arrBank1) and set(v['bank2']) == set(arrBank2) and int(
        v['layer']) % 2 == (l + 1) % 2, g.nodes(data=True))
    if len(ppp) == 0:
        g.add_node(currentNodeNo, bank1=arrBank1, bank2=arrBank2, layer=l + 1)
        g.add_edge(previousNodeNo, currentNodeNo)
        currentNodeNo += 1
        if set(arrBank2) == set(rolesArr):
            goalReached = True
            goalNodeNo = currentNodeNo - 1


roles = raw_input("Input characters separated by space : ")
rolesArr = set(roles.split())
# rolesArr =set(['F','W','G','C'])
bank1Status = rolesArr
driver = raw_input("Input characters who can drive the boat : ")
driverArr = set(driver.split())
# driverArr = set(['F'])
boatCapacity = int(raw_input("Input the boat capacity : "))

nonDriverArr = rolesArr - driverArr

if (not driverArr <= rolesArr):
    print("Drivers must be a subset of characters")
    exit(0)
else:
    print("Initial state : " + str(map(str, rolesArr)))

restricktedBank = raw_input("Input restricted combinations on riverbanks : ")
# restricktedBank ="W,G W,G,C"
pairList = restricktedBank.split()
for i in pairList:
    arr = []
    j = i.split(',')
    for k in j:
        arr.append(k)
    restricktedRiverbank.append(arr)

restrickted_Boat = raw_input("Input restricted combinations on boat : ")
# restrickted_Boat = ''
pairList2 = restrickted_Boat.split()
for i in pairList2:
    arr = []
    j = i.split(',')
    for k in j:
        arr.append(k)
    restricktedBoat.append(arr)

g.add_node(currentNodeNo, bank1=map(str, rolesArr), bank2=[], layer=0)
currentNodeNo += 1
previousNodeNo += 1

l = 0
while (not goalReached):
    layer = filter(lambda (k, v): v['layer'] == l, g.nodes(data=True))
    for b in layer:
        previousNodeNo = b[0]
        bank1Status = b[1]['bank1']
        bank2Status = b[1]['bank2']
        if l % 2 == 0:
            temp = generatePermutations(bank1Status)
            temp = validatePermutations(temp, l)
            for i in temp:
                arrBank1 = list(set(bank1Status) - set(i))
                arrBank2 = bank2Status + i
                addNodeIfNotExist(arrBank1, arrBank2, l)
        else:
            temp = generatePermutations(bank2Status)
            temp = validatePermutations(temp, l)
            for i in temp:
                arrBank1 = bank1Status + i
                arrBank2 = list(set(bank2Status) - set(i))
                addNodeIfNotExist(arrBank1, arrBank2, l)
    l += 1

colours = ['red', 'green', 'blue', 'cyan', 'blueviolet', 'orange', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
           'beige', 'bisque','limegreen','sandybrown','deeppink','tomato','navy','coral']
applyColours = []
labeldict = {}
for i in range(currentNodeNo - 1):
    labeldict[i + 1] = str(g.node[i + 1]['bank1']) + " | " + str(g.node[i + 1]['bank2']) + " + layer " + str(
        g.node[i + 1]['layer'])
    index = int(g.node[i + 1]['layer'])
    applyColours.append(colours[index])

path = nx.shortest_path(g, source=1, target=goalNodeNo)
print "iteration bank1 bank2"
j=1
for i in path:
    print str(j)+" "+str(g.node[i]["bank1"]) + " | " + str(g.node[i]["bank2"])
    j+=1
path_edges = zip(path, path[1:])
pos = nx.spring_layout(g)
nx.draw(g, pos, labels=labeldict, node_color=applyColours)
nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='r', width=4)
plt.show()
