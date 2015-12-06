from __future__ import division
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as ny


p_i = 0.05 # infection probability
results = []
n = 1024			#numbers of nodes in the network
k	= 1 
k_end 	= 20
round_num = 0
S = []
round_results=[]
def setRound_num(num):
	global round_num
	round_num= num

def spread(g,n):
	global p_i, S
	mean_coverage =0
	
	temp_boarder=[]
	temp_infected=[]
		#p_i=0.05
		#dummy_g = g.copy()
	#for i in range(50):
	for node in S:
		temp_boarder.append(node)
		#dummy_g.node[node]['state']=1
		#print("spread doing %d" %len(S))
	# while (len(temp_boarder)!=0):
	# 	current_vertex = temp_boarder.pop(0)
	# 	for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
	# 		#if(dummy_g.node[i]['state'] == 0 ):
	# 		if(i not in temp_boarder):
	# 			if(rd.random() < p_i):	
	# #				print("adding to boarder")		#check if the testing node is infected or not and #The coin flip to se if infected
	#				temp_boarder.append(i)
	
	temp_boarder.append(n)
	#for i in dummy_g.neighbors(n):
	#	if(dummy_g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
	#		if(rd.random() < p_i):					#The coin flip to se if infected	
	#			dummy_g.node[i]['state'] = 1
	#			temp_boarder.append(i)
	#			temp_infected.append(i)
	
	while (len(temp_boarder)!=0):
		current_vertex = temp_boarder.pop(0)
		temp_infected.append(current_vertex)
		mean_coverage+=1
		for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
			#if(dummy_g.node[i]['state'] == 0 ):
			if(i not in temp_boarder and i not in temp_infected):
				if(rd.random() < p_i):
					#check if the testing node is infected or not and The coin flip to se if infected
					temp_boarder.append(i)
#		del temp_boarder[:]
#		del temp_infected[:]		
#		print(len(temp_boarder))	
#	print("temp boarder: %d" %len(temp_boarder))
	#print("temp infected: %d" %len(temp_infected))
#	coverage = ((len(temp_infected)+len(temp_boarder))/128.0)
#	return len(temp_infected)
	return(mean_coverage)

#This is the seed selection algorithm,
def seed_selection(G, k):
	global S
	#Finding the degree distribution.
	#sort the graph in respect of degree
	temp_s = []
	for node in g.nodes_iter():
		degree=G.degree(G.node[node]).values()
		T_seed = [degree, node]
		temp_s.append(T_seed)

	temp_s.sort()

	for i in range(k):
		S.append(temp_s[i][1])




def initialize():#initialize the simulation
	global g, init_seed, nextg, n, k, infected, boarder, coverage, results, round_num, S, k_counter, round_results,position

	infected, boarder = [], []
	k_counter =0	
	#g = nx.karate_club_graph()		#can't use karate club graph, there are only 34 nodes there. Need to manually add the nodes.
	#------------------------------Create the graph, 128nodes. not sure how many edges.-----------------------------------
	total_edge = 0
	g = nx.Graph()
	
	for i in range(n):
		g.add_node(i)
	with open("adjacency.txt") as f:
		content = f.readlines()		
		for i in range(n):
			for j in range(i+1, n):
				if(content[i][j] ==	 '1'):
					g.add_edge(i,j)
					total_edge+=1
	

	#print("total starting seed")
	#print(len(S))
	#print("Total edge:")
	#print(total_edge)
	#--------------------------------------------------------------------------------------
	round_num +=1
	counter = 0
	coverage = 0
	#----------------------Seed selection algorithm----------------------------------------------
	
#	for i in g.nodes_iter():
#		if(i in S):
#			#print(len(S))
#			g.node[i]['state']=1
#			boarder.append(i)
#		else:
#			g.node[i]['state'] = 0
	#part A: Seed selectio.
	
	if(len(S)<k):
		position=nx.spring_layout(g)
		proxy_g = g.copy()
		seed_selection(proxy_g, k)

		for node in S:
			g.node[node]['state'] = 1
			boarder.append(node)
	#	nextg.node[S[k-1]]['state'] =1
	#nextg = g.copy()
	
	for i in g.nodes_iter():	#here we jsut select the 10 first nodes as seed
		if(i not in S):
			g.node[i]['state'] = 0
		else:
			g.node[i]['state'] = 1
			boarder.append(i)
	# if(len(init_seed)==0):
	# 	proxy_g = g.copy()
	# 	init_seed = seed_selection(proxy_g, k)
	g.pos = position
	#if(len(S)==k):
	#	for x in range(k):
	#	 	i = S[x]
#		 	g.nodes[i]['state'] = 1
	#	 	boarder.append(i)
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
	global g, nextg, infected, boarder, coverage, n, k_counter, S, k, results, round_num, round_results
	
	#part b
	
	if (len(boarder)==0):
		round_results.append(coverage)
		#print(round_results)

		if(round_num == 50):
			counter=0
			for item in round_results:
				counter+=item
			#print(len(round_results))
			spread_p =counter/len(round_results)
			results.append(spread_p)
	#		print(results)
			text_file = open("degree_result_multi_run.txt", "w")
			for lines in results:
				text_file.write("%s\n" % lines )
	 		text_file.close()

	 		k+=1
	 		del round_results[:]
	 		del S[:]	
			setRound_num(0)
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
	 	infected.append(current_vertex)
			
	 	coverage = ((len(infected)+len(boarder))/n)
 	
 	if(k==k_end+1):
 		sys.exit("Simulation complete")

	g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
	