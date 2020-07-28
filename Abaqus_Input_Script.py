from abaqusConstants import *


nodes = []
edges = []

#Paste path to Nodes.txt here, make sure to use double slashes between folders
with open('C:\\Users\\Christopher\\Desktop\\Geodesic Dome Calculator\\nodes.txt') as fp:
    line = fp.readline()
    count = 0
    while line:
        xy = line.split(' ')
        xy = (float(xy[0]), float(xy[1]), float(xy[2].rstrip('\n')))
        #print(xy)
        nodes.append(xy)
        line = fp.readline()

#Paste path to Edges.txt here, make sure to use double slashes between folders
with open('C:\\Users\\Christopher\\Desktop\\Geodesic Dome Calculator\\Edges.txt') as fp:
    line = fp.readline()
    count = 0
    while line:
        xy = line.split(' ')
        xy = (int(xy[0]), int(xy[1].rstrip('\n')))
        #print(xy)
        edges.append(xy)
        line = fp.readline()


for i in edges:
    print(i)
#print(edges)
p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, type=DEFORMABLE_BODY)

#Paste the list of nodes generated by DomeGenerator.py here

for j in range(len(nodes)):
    dtm = p.DatumPointByCoordinate(coords=nodes[j])

#Paste the list of nodes generated by DomeGenerator.py here

d = p.datums
for i in edges:
     p.WirePolyLine(points=((d[i[0]], d[i[1]])), mergeType=IMPRINT)
