import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as ny

p_i = 0.15 # infection probability
results = []
n = 128.0						#numbers of nodes in the network
k = 10 
round_num = 0
S = []

def spread(g,n):
	global p_i
	temp_boarder=[]
	coverage=0
	#p_i=0.05
	dummy_g = g.copy()
	for node in dummy_g.nodes_iter():
		if(dummy_g.node[node]['state']==1):
			temp_boarder.append(node)

	for i in dummy_g.neighbors(n):
		if(dummy_g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
			if(rd.random() < p_i):					#The coin flip to se if infected	
				dummy_g.node[i]['state'] = 1
				temp_boarder.append(i)


	while (len(temp_boarder)!=0):
		current_vertex = temp_boarder.pop(0)
		for i in dummy_g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(dummy_g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
					dummy_g.node[i]['state'] = 1
					temp_boarder.append(i)
		
		coverage = ((len(infected)+len(boarder))/128.0)
	return coverage

#This is the seed selection algorithm,
def seed_selection(G, k):
	temp_result =[]
	for n in G.nodes_iter():
		if(G.node[n] not in S):
			coverage = spread(G, n)
			optimal_set =[coverage, n]
			temp_result.append(optimal_set)
	temp_result.sort()
	best_result = temp_result[0]
	G.node[best_result[1]]['state'] = 1
	S.append(best_result[1])

	# for i in range(k):	#should find total of k nodes.
	# 	for n in G.nodes_iter():
	# 		if(g.node[i] not in S):
	# 			coverage = spread(G, n, infected, boarder)
	# 			optimal_set = [coverage, n ]


	# 			if(len(S)<10):
	# 				S.append(optimal_set)
	# 			elif(S[9][0]>coverage):
	# 				S[9] = optimal_set
	# 				S.sort()
	# 	S.append()


def initialize():#initialize the simulation
	global g, init_seed, nextg, n, k, infected, boarder, coverage, results, round_num, S, k_counter
	infected, boarder = set(), []
	k_counter =0
	n =128.0
	k =10
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
	# print("total starting seed")
	# print(len(S))
	# print("Total edge:")
	# print(total_edge)
	#--------------------------------------------------------------------------------------
	round_num +=1
	counter = 0
	coverage = 0
	#----------------------Seed selection algorithm----------------------------------------------
	

	for i in g.nodes_iter():		#here we jsut select the 10 first nodes as seed
		g.node[i]['state'] = 0

	nextg = g.copy()
	
	# if(len(init_seed)==0):
	# 	proxy_g = g.copy()
	# 	init_seed = seed_selection(proxy_g, k)
	if(len(S)==k):
		for x in range(k):
		 	i = S[x]
		 	g.node[i]['state'] = 1
		 	boarder.append(i)
	nextg = g.copy()

	# print("total seed:")
	# print(len(init_seed))


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

#To generate a program that shows the picking of the nodes, Might have to have the update to work in different stages, If the lan(S)==k, start diffusion. 
#If not, pick the nodes.

def update():
	global g, nextg, infected, boarder, coverage, n, k_counter, S
	# #part A: Seed selectio.

	if(k_counter < k and len(S)<k ):
		seed_selection(g, k_counter)
		boarder.append(S[k_counter])
		g.node[S[k_counter]]['state'] =1
		nextg.node[S[k_counter]]['state'] =1
		k_counter+=1
	else:
		if (len(boarder)==0):
			results.append(coverage)
			print(results)
		
	 		text_file = open("greedy_result.txt", "w")
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
		 				g.node[i]['state'] = 1
		 				nextg.node[i]['state']=1
		 				boarder.append(i)
		 	infected.add(current_vertex)
			
		 	coverage = ((len(infected)+len(boarder))/128.0)

		g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
	