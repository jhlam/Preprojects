from __future__ import division
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as ny
import sys
from random import choice

p_i =0.05					# infection probability
results = []
#n = 128			#numbers of nodes in the network
#n=512
n=1024
#avg step before finish: small =20 result =15
#avg step before finish: medium = 179 	=	125
#avg step before finish: LARGE = 271	= 190
k = 1
k_end= 20
round_num = 0
init_seed =[]
S=[]
round_results=[]
total_vertex=0
step=0
end_step=190

def setRound_num(num):
	global round_num
	round_num=num

def spread(g,n):
	global p_i
	temp_boarder =[]
	temp_infected =[]
	mean_coverage=0

	temp_boarder.append(n)

	while (len(temp_boarder)!=0):
		current_vertex = temp_boarder.pop(0)
		temp_infected.append(current_vertex)
		mean_coverage+=1
		for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
			if(i not in temp_boarder and i not in temp_infected ):			#check if the testing node is infected or not
				if(rd.random() < p_i):					#The coin flip to se if infected
#					
					temp_boarder.append(i)

	return mean_coverage


def seed_selection(G):
	global S
	
	random_node = choice(G.nodes())
	S.append(random_node)
	#	print("Finding random seed")

	print("current amount of seed:%i" %len(S))


def initialize():#initialize the simulation
	global g, init_seed, nextg, n, k, infected, boarder, coverage, results, round_num, position, total_vertex
	infected, boarder = [], []	
	#g = nx.karate_club_graph()		#can't use karate club graph, there are only 34 nodes there. Need to manually add the nodes.
	#------------------------------Create the graph, 128nodes. not sure how many edges.-----------------------------------
	if(n==128):
		filename="adjacency_small.txt"
	elif(n==512):
		filename="adjacency_medium.txt"
	else:
		filename="adjacency_large.txt"
	
	total_edge = 0
	g = nx.Graph()
	for i in range(n):
		g.add_node(i)
	with open(filename) as f:
		content = f.readlines()		
		for i in range(n):
			for j in range(i+1, n):
				if(content[i][j] ==	 '1'):
					g.add_edge(i,j)
					total_edge+=1
					
	
	#--------------------------------------------------------------------------------------

	
	
	for nodes in range(n):
		if(nx.degree(g, nodes)==0):
			g.remove_node(nodes)
		
	
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
		print("total node was: %s" %nx.number_of_nodes(g))
		print("total edge was: %s" %nx.number_of_edges(g))

		position= nx.spring_layout(g)
		seed_selection(g )

		for node in S:
			g.node[node]['state'] = 1
			boarder.append(node)
			

	g.pos =position
	nextg = g.copy()


def observe():
	global g, nextg, n, k, coverage, round_num
	cla()
	nx.draw(g, cmap = cm.binary,vmin = 0, vmax = 2,
       	node_color = [g.node[i]['state'] for i in g.nodes_iter()],
	       	pos = g.pos,with_lables = True)
	
	title(round_num)


def update():
	global g, nextg, infected, boarder, coverage, n, k_counter,S, k, results, round_num, round_results, total_vertex, step, end_step
	step+=1
	if(k==k_end+1):
		histogram= nx.degree_histogram(g)
	
		if(n==128):
			text_file = open("step_small_random_result_multi_run.txt", "w")
		elif(n==512):
			text_file = open("step_medium_random_result_multi_run.txt", "w")
		else:
			text_file = open("step_large_random_result_multi_run.txt", "w")
			
		text_file.write("total node was: %s \n" %nx.number_of_nodes(g))
		text_file.write("total edge was: %s \n" %nx.number_of_edges(g))

		for lines in results:
			text_file.write("%s\n" % lines )
	
		text_file.write("Seednode was: ")	
		for seed in S:
			text_file.write("node_%s, " % seed )
	
		text_file.write("Histogram: ")	
		for i in histogram:
			text_file.write("%s ," % i )

		text_file.close()

		sys.exit("simulation complete")

	if (len(boarder)==0 or step==end_step):
		round_results.append(coverage)
		#print(results)
		if(round_num == 50	):
			counter=0
			for item in round_results:
				counter+=item
			spread_p = counter/len(round_results)
			results.append(spread_p)

		
			k+=1
			del round_results[:]
			#del S[:]
			setRound_num(0)

		step =0
		initialize()
	else:
		current_vertex = boarder.pop(0)
		if(current_vertex not in infected):
			for i in g.neighbors(current_vertex):		#iterate over the current node's neighbour
				if(g.node[i]['state'] == 0 ):			#check if the testing node is infected or not
					if(rd.random() < p_i):					#The coin flip to se if infected
						nextg.node[i]['state'] = 1 
						g.node[i]['state'] = 1
						boarder.append(i)
			
			infected.append(current_vertex)
			
			coverage = ((len(infected))/len(g.nodes()))


	g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
		
	