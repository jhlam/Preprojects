import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

p_i = 0.5 # infection probability

def bfs(g, start):
	visited, queue = set(), [start]
	while queue:
		vertex = queue.pop(0)
		if(vertex['state']==0):#checks if the vertex is infected
			vertex['state'] = 1 if random() < p_i else 0
			if vertex = not in visited:
				visited.add(vertex)
				queue.extend(graph[vertex] - visited)
		else:
			visited.add()
	return visited


def initialize():#initialize the simulation
	global g, nextg,n ,k
	g = nx.karate_club_graph()#can't use karate club graph, there are only 34 nodes there. Need to manually add the nodes.
	n = 100	#numbers of nodes in the network
	k = 10 	#number of seeds


	g.pos = nx.spring_layout(g)
	for i in g.nodes_iter():
		g.node[i]['state'] = 0
	
	nextg = g.copy()


def observe():
	global g, nextg, n, k
	cla()

	nx.draw(g, cmap = cm.binary,vmin = 0, vmax = 1,
         	node_color = [g.node[i]['state'] for i in g.nodes_iter()],
         	pos = g.pos,with_lables = True)
	#nx.draw(g, g.pos, with_labels = True)


def update():
	global g
	#This is the code for the infections model. this is a SI model.
	a = rd.choice(g.nodes())# chosses a random node?
	if g.node[a]['state'] == 0: # if susceptible
		b = rd.choice(g.neighbors(a))
		if g.node[b]['state'] == 1: # if neighbor b is infected
			g.node[a]['state'] = 1 if random() < p_i else 0


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
\