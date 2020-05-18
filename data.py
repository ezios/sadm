#Mahaman bachir Attouman Ousmane
#Adediran Flore
#Ali Abakar
#Yves Fernand Nga Ngono
from re import findall
import numpy as np

def read_data(instance):
	# lecture des instances de test , formatage des donnees
	try:
		f = open(instance,"r")
	except: 
		print("No Such file \n syntaxe: myprogram input_file exec_time output_file ")


	#importer les chiffre en supprimant tous les espaces et retour chariot
	data=findall("\d+",f.read())

	for i in range(len(data)):  
	#conersion en entier
		data[i] = int(data[i])

	n,m=data[0],data[1]
	#lecture de la dimension et du nombres d elements
	poids=np.zeros((m,n),dtype=int)

	profits=np.array(data[2:n+2])
	#les coefficients Cj
	contraintes = data[n+2:n+2+m]

	temp = data[n+2+m:]
	for i in range(m):
		poids[i] = temp[n*i:n*i+n]
    #les poids sont mis dans un tableau		
	return (n,m,profits,contraintes,poids)