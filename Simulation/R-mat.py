import random as rd
import math

a_p = 0.3
d_p = 0.2
b_p = 0.25
v = 128
Matrix = [[0 for x in range(v)] for x in range(v)] 

def creat_directed_rmat(A, n):
	x_start = A[0]
	x_end	= A[1]
	y_start	= A[2]
	y_end	= A[3]
	new_n   = n/2
	noise   = rd.uniform(0, 0.1)*(-1*rd.getrandbits(1))#Might be good to generate some noise for each rnus.
	
	if(x_end - x_start <= 1):
		Matrix[x_start][y_start] = 1

	else:
		if(rd.random()< a_p+noise):#IF A
			sub_matrix = [x_start, x_start+new_n, y_start, y_start+new_n]
			creat_directed_rmat(sub_matrix, new_n)

		elif(rd.random()<d_p+noise):#If D
			sub_matrix = [x_start+new_n, x_end, y_start+new_n, y_end]
			creat_directed_rmat(sub_matrix, new_n)
			
                
		elif(rd.random()<b_p+noise): #If B
			sub_matrix = [x_start+new_n, x_end, y_start, y_start+new_n]
			creat_directed_rmat(sub_matrix, new_n)
		
		else:                   #If C
			sub_matrix = [x_start, x_start+new_n, y_start+new_n, y_end]
			creat_directed_rmat(sub_matrix, new_n)

	
def flip_flop(y_amount):
	for y in range(y_amount):
		for x in range(y):
			Matrix[y][x]= Matrix[x][y]

	for i in range(y_amount):
		Matrix[i][i] = 1

def init(amount_edge):
	
	text_file = open("adjacency.txt", "w")

	for edges in range(amount_edge):
		creat_directed_rmat([0,v,0,v], v)
        
	flip_flop(v)

	for row in Matrix:
		for cell in row:
			text_file.write("%s" % cell)
		text_file.write('\n')

	text_file.close()
	print("Done!")
