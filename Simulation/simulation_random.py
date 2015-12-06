from __future__ import division
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as ny
import sys
from random import choice

p_i = 0.05 					# infection probability
results = []
n = 1024				#numbers of nodes in the network
k = 1
k_end= 20
round_num = 0
init_seed =[]
S=[]
round_results=[]

def setRound_num(num):
	global round_num
	round_num=num

def spread(g,n):
	global p_i
	temp_boarder =[]
	temp_infected =[]
	mean_coverage=0
#	for i in range(50):
#	dummy_g = g.copy()
#	for i in neighbors(n):
#		if( g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
#				if(rd.random() < p_i):					#The coin flip to se if infected	
#					dummy_g.node[i]['state'] = 1
	#					temp_boarder.append(i)
	temp_boarder.append(n)

	while (len(temp_boarder)!=0):
		current_vertex = temp_boarder.pop(0)
		temp_infected.append(current_vertex)
		mean_coverage+=1
		for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(i not in temp_boarder and i not in temp_infected ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
#					dummy_g.node[i]['state'] = 1
					temp_boarder.append(i)
#	del temp_infected[:]
	#coverage = ((len(temp_infected)+len(temp_boarder))/128.0)
		
	return mean_coverage


def seed_selection(G, k):
	global S
	
	for i in range(k):
		random_node = choice(G.nodes())
		S.append(random_node)
	#	print("Finding random seed")

	print("current amount of seed:%i" %len(S))


def initialize():#initialize the simulation
	global g, init_seed, nextg, n, k, infected, boarder, coverage, results, round_num, position
	infected, boarder = [], []	
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
		position= nx.spring_layout(g)
		proxy_g = g.copy()
		seed_selection(proxy_g, k)

		for node in S:
			g.node[node]['state'] = 1
			boarder.append(node)
			#S.append(node)
			#print("Painting the seed")

	g.pos =position

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

			text_file = open("random_result_multi_run.txt", "w")
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
		infected.append(current_vertex)
		
		coverage = ((len(infected)+len(boarder))/n)

	if(k==k_end+1):
		sys.exit("simulation complete")

	g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
		
