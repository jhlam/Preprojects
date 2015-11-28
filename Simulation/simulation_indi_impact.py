from __future__ import division
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
k = 1
k_end= 20
round_num = 0
init_seed =[]
S=[]
round_results=[]

def setRound_num(n):
	global round_num
	round_num=n

def spread(g,n):
	global p_i
	coverage=0
	temp_boarder =[]
	temp_infected =set()

	dummy_g = g.copy()
	for i in dummy_g.neighbors(n):
		if(dummy_g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected	
					dummy_g.node[i]['state'] = 1
					temp_boarder.append(i)
	temp_infected.add(n)

	while (len(temp_boarder)!=0):
		current_vertex = temp_boarder.pop(0)
		for i in dummy_g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(dummy_g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
					dummy_g.node[i]['state'] = 1
					temp_boarder.append(i)
		temp_infected.add(current_vertex)
		
	#coverage = ((len(temp_infected)+len(temp_boarder))/128.0)
	
	return len(temp_infected)


def seed_selection(G, k):
	global S
	temp_S=[]
	for i in range(k):
		for n in G.nodes_iter():
			coverage = spread(G, n)
			optimal_set = [coverage, n ]
			
			if(len(temp_S)<k):
				temp_S.append(optimal_set)
			
			elif(temp_S[0][0] > coverage):
				temp_S[0] = optimal_set
			
			temp_S.sort()
	
	

	print("current amount of seed:%i" %len(temp_S))
	return temp_S


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
	#print("Total edge:")
	#print(total_edge)
	#--------------------------------------------------------------------------------------

	round_num +=1
	counter = 0
	coverage = 0
	#----------------------Seed selection algorithm----------------------------------------------
	for i in g.nodes_iter():	#here we jsut select the 10 first nodes as seed
		if(i not in S):
			g.node[i]['state'] = 0
		else:
			g.node[i]['state'] = 1
			boarder.append(i)


	if(len(S)<k):
		proxy_g = g.copy()
		temp_S = seed_selection(proxy_g, k)

		for node in temp_S:
			i = node[1]
			g.node[i]['state'] = 1
			boarder.append(i)
			S.append(i)


	nextg = g.copy()

	#print("total seed:")
	#print(len(init_seed))


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
	global g, nextg, infected, boarder, coverage, n, k_counter,S, k, results, round_num, round_results

	if (len(boarder)==0):
		round_results.append(coverage)
		#print(results)
		if(round_num == 50	):
			counter=0
			for item in round_results:
				counter+=item
			spread_p = counter/len(round_results)
			results.append(spread_p)

			text_file = open("indi_result_multi_run.txt", "w")
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
					nextg.node[i]['state'] = 1 
					g.node[i]['state'] = 1
					boarder.append(i)
		infected.add(current_vertex)
		
		coverage = ((len(infected)+len(boarder))/n)

	if(k==k_end+1):
		sys.exit("simulation complete")

	g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
		
