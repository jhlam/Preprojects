import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as ny
import sys

p_i = 0.15 # infection probability
results = []
n = 128.0						#numbers of nodes in the network
k = 10 
round_num = 0
init_seed =[]

def spread(g,n):
	global p_i
	coverage=0
	boarder =[]
	infected =set()
	for i in g.neighbors(n):
		if(g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected	
					g.node[i]['state'] = 1
					boarder.append(i)
		infected.add(n)

	while (len(boarder)!=0):
		current_vertex = boarder.pop(0)
		for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
					g.node[i]['state'] = 1
					boarder.append(i)
		infected.add(current_vertex)
		
		coverage = ((len(infected)+len(boarder))/128.0)
	return coverage


def seed_selection(G, k):
	S = []
	for i in range(k):
		for n in G.nodes_iter():
			coverage = spread(G, n)
			optimal_set = [coverage, n ]

			if(len(S)<10):
				S.append(optimal_set)
			elif(S[9][0]>coverage):
				S[9] = optimal_set
				S.sort()
	return S


def initialize():#initialize the simulation
	global g, init_seed, nextg, n, k, infected, boarder, coverage, results, round_num
	infected, boarder = set(), []	
	#g = nx.karate_club_graph()		#can't use karate club graph, there are only 34 nodes there. Need to manually add the nodes.
	#------------------------------Create the graph, 128nodes. not sure how many edges.-----------------------------------
	total_edge = 0
	g = nx.Graph()
	for i in range(128):
		g.add_node(i)
	with open("adjacency.txt") as f:
		content = f.readlines()		
		for i in range(128):
			for j in range(i+1, 128):
				if(content[i][j] ==	 '1'):
					g.add_edge(i,j)
					total_edge+=1
	g.pos = nx.spring_layout(g)
	print("Total edge:")
	print(total_edge)
	#--------------------------------------------------------------------------------------

	round_num +=1
	counter = 0
	coverage = 0
	#----------------------Seed selection algorithm----------------------------------------------
	for i in g.nodes_iter():		#here we jsut select the 10 first nodes as seed
		g.node[i]['state'] = 0

	if(len(init_seed)==0):
		proxy_g = g.copy()
		init_seed = seed_selection(proxy_g, k)

	for x in range(k):
		i = init_seed[x][1]
		g.node[i]['state'] = 1
		boarder.append(i)
	nextg = g.copy()

	print("total seed:")
	print(len(init_seed))


def observe():
	global g, nextg, n, k, coverage, round_num
	cla()
	#nx.draw_random(g)
	nx.draw(g, cmap = cm.binary,vmin = 0, vmax = 2,
       	node_color = [g.node[i]['state'] for i in g.nodes_iter()],
       	pos = g.pos,with_lables = True)
	#nx.draw(g, g.pos, with_labels = True)
	
	#nx.draw_circular(g, cmap = cm.binary,vmin = 0, vmax = 1,
	#		node_color = [g.node[i]['state'] for i in g.nodes_iter()],with_lables = True)
	
	title(round_num)


def update():
	global g, nextg, infected, boarder, coverage, n
	if (len(boarder)==0):
		results.append(coverage)
		print(results)
		
		text_file = open("result.txt", "w")
		for item in results:
			text_file.write("%s\n" % item )
		text_file.close()

		#np.savetxt('Output.txt', results, delimiter=",")   # X is an array

		initialize()
	else:
		current_vertex = boarder.pop(0)
		for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
					nextg.node[i]['state'] = 1 
					g.node[i]['state'] = 1
					boarder.append(i)
		infected.add(current_vertex)
		
		coverage = ((len(infected)+len(boarder))/n)

		g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
		