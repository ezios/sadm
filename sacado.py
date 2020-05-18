#Mahaman bachir Attouman Ousmane
#Adediran Flore
#Ali Abakar
#Yves Fernand Nga Ngono
from re import findall
import numpy as np
import time 
from data import read_data
import sys
try:
	input_file = sys.argv[1]
	exec_time = sys.argv[3]
	output_file = sys.argv[2]
except:
	print("error, usage sacado.py nom_instance temp_execution fichier_de_sortie")
	sys.exit()
try:
	ofile = open(output_file,"w")
except:
	print("No Output file \n usage: myprogram input_file exec_time output_file ")
	sys.exit()
try:
	exec_time=int(exec_time)
except:
	print("Error time must be integer in seconds \n syntaxe: myprogram input_file exec_time output_file ")
	sys.exit()
start_time = time.time()

def best_move():
	global s,s0,c,constraints,weight,x,n,m 

	b =np.zeros(m)
	w =np.zeros(m,dtype=float)
	s=np.zeros((m,n),dtype = float)
	new_constraints = np.zeros(m,dtype = float)

    #calcul de b' contraintes initiales - les poids des objets  par dimension
    #pour les contraintes violées b' est negatif sinon positif , on calcule des coefficients
	for i in range(m):
		b[i] = constraints[i] - np.sum(weight[i]*x)

		if b[i] > 0 :
			w[i] = (1/b[i])
		else:
			w[i] = (2 + abs(b[i]))

	#ici on recalcule les coefficients des poids  
	for i in range(m):		
		s[i] = w[i]*weight[i] 
		new_constraints[i]= w[i] * constraints[i]

	#Calcul des d'une contrainte de substitution unique pour les m sac
	s = np.sum(s,axis=0)
	s0 = sum(new_constraints)
	#la fonction retourne le rapport valeur et poids des objets dans un tableau pour evaluation du mouvement. 
	return c/s


def initial_solution()	:
	#calcul d'une solution pour la premiere contrainte de substitution par methode gloutonne
	global s,s0
	i=0
	sack_capacity = 0
	size = len(s)
	x= np.zeros(size,dtype=int)
	#on n'empile les éléments tant que le sac n'est pas plein
	while i < size : 
		if sack_capacity <= s0:
			sack_capacity += s[i]
			x[i] = 1
			i+=1
		else:
	#si pour un poids la capacite du sac est depassee ,l'element est retire et on continue l'iteration
			sack_capacity -= s[i]
			i+=1
	return x



def remove (values_over_weight,tabu_list)	:

	global x
	i=0
	#tri croissant du rapport valeur/poids
	temp = values_over_weight.argsort()
	temp = list(temp)
	for tabu in tabu_list:
		if tabu in temp:
			temp.remove(tabu)
	#ne pa choisir l'element s'il est deja 0 
	while x[temp[i]] == 0:
		i+=1
	#la boucle s'est arrete ,  le plus petit element a 1 est mis a 0
	x[temp[i]] = 0
	return temp[i]


def put(values_over_weight,tabu_list) :
	global x 	
	i=0
	#tri decroissant

	temp = values_over_weight.argsort()[::-1]

	temp = list(temp)
	for tabu in tabu_list:
		if tabu in temp:
			temp.remove(tabu)
	while x[temp[i]] == 1:
		i+=1
	#la boucle s'est arrete ,  le plus grand element a 0 est mis a 1
	x[temp[i]] = 1
	return temp[i]


def real_evaluate():
	global x,constraints,weight,m 

	for j in range(m):
		if sum( x*weight[j] ) > constraints[j]:
			return 0
	  
	return 1

def find_best_solution(param):
		global x 
		gain = 0
		best = -1
		for i in range(n):
			if (x[i]==0 and c[i] > gain):
				x[i]=1
				if not real_evaluate()*param:
					x[i]=0
				else:
					best = i
					gain = c[i]
					x[i] =0	

		return best


def find_best_solution2(param):
		global x 
		gain = 10000
		best = -1
		for i in range(n):
			if (x[i]==1 and  c[i] < gain):
				x[i]=0
				if not real_evaluate()*param:
					x[i]=1
				else:
					best = i
					gain = c[i]
					x[i] =1

		return best
def critical_constructive_proc():
	global c,x,latest_move
	x[latest_move] = 0
	sol = find_best_solution(1)
	if sol!=-1:
		x[sol] = 1
	
	x[latest_move] = 1
	sol = find_best_solution2(1)
	if sol!=10000:
			x[sol] = 0


def print_procedure(fin):
	global c
	ofile.write(str(np.sum(c*fin))+" "+str(sum(fin)))
	ofile.write('\n')
	for i in range(n):
		if fin[i] ==1:
			ofile.write(str(i)+" ")

n,m,c,constraints,weight = read_data(input_file)

x = np.random.randint(2,size=n)
s=0
s0=0
c_tabu_list = []
d_tabu_list = []
solution_finale=0
feasible=real_evaluate()
iteration=0




while((time.time() -start_time) < exec_time-0.5):
	iteration+=1

	for _ in range(5): 
		move_choice=best_move()
		latest_move=remove(move_choice,c_tabu_list)

	feasible = real_evaluate()
	d_tabu_list.append(latest_move)

	while feasible	:
		move_choice = best_move()
		latest_move = put(move_choice,d_tabu_list)
		feasible=real_evaluate()

	c_tabu_list.append(latest_move)
	critical_constructive_proc()

	if iteration%7==0:
		c_tabu_list=[]
		d_tabu_list=[]

	if real_evaluate():	

		sol_temp = np.sum(c*x)
		if solution_finale<sol_temp:
			solution_finale = sol_temp
			fin = x.copy()
	

print_procedure(fin)		
print(solution_finale , time.time() - start_time)