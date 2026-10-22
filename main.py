'''
Shawn Arreguin
9/7/26
Main script
'''

import NJ
import sys
import argparse


def makeDaTree(Names, BigList):
	'''
	Dis make da tree.
	This will run through a while loop until all taxa are connected.
	Once you have three taxa left, we perform a final branch estimation.
	'''


	Node=[]
	Tree=[]

	count=len(Names)
	print(count)
	
	while count >= 3:

		if count == 3:

			branchA, branchB, branchC = NJ.branchEst3(BigList)
			
			tmpT="("+Names[0]+":"+str(branchA)+",("+Names[1]+":"+str(branchB)+","+Names[2]+":"+str(branchC)+"):0);"

			print(tmpT)

			count=count-1


		else:

			q, min_val, best_i, best_j, best_row, best_col = NJ.qMatrix(Names, BigList) #here we get the best that pair

			branchA, branchB = NJ.branchEst2(BigList, best_i, best_j, best_row, best_col) #here we get the branch lengths


			tmpT="("+Names[best_i]+":"+str(branchA)+","+Names[best_j]+":"+str(branchB)+")"



			Names, BigList = NJ.updateDatDistancM(Names, BigList, q, best_i, best_j) #here we update the distance matrix to reflect the new pairing
			
			del Names[0]
			Names.insert(0,tmpT)

			count = len(Names)




if __name__ == "__main__":


	#Options
	parser = argparse.ArgumentParser(description="Neighbor Joining Tree Program")

	parser.add_argument("-f","--file",type=str,help="File to be run through the program. By default, this is treated as a FASTA.")
	parser.add_argument("-d","--distance", action='store_true',
		help="This designates that you would like to use a premade distance matrix rather than a FASTA as the input. TSVs or CSVs are accepted.")

	#Help check
	args = parser.parse_args()

	#Help check when only main is given
	if len(sys.argv) == 1:
		parser.print_help()
		print(":(")
		sys.exit()


	#Da file
	file = args.file



	#Check if distance matrix or FASTA is given
	if args.distance:

		#If we have a distance matrix (CSV/TSV) to start, we'll need to read it in
		#We'll need to save rows into lists and stack them into a BigList
		#The first row will be saved as Names and the first element of each list will be discarded

		if file[-4:].lower() == ".tsv":

			distM=open(file,"r")
			Names, BigList = NJ.tsvDist(distM)

			makeDaTree(Names,BigList)


		elif file[-4:].lower() == ".csv":

			distM=open(file,"r")
			Names, BigList = NJ.csvDist(distM)

			makeDaTree(Names,BigList)

		else:
			print(file[-4:])
			print("Oooof! The -d option uses a distance matrix rather than a FASTA file. Applicable files types are TSVs and CSVs")


	
	else: #FASTA option

		fasta=open(file,"r")
		Names, BigList = NJ.distMatrix(fasta)


		makeDaTree(Names,BigList)
		


#How tf do we incorporate nodes in this bitch?

#Thought, so we pull a node and we name it. inside the node we'll call tree traveler. Tree travler will give us all pieces that we label as sisiter etc.
#During this process, we can also save look for node names in the tree.
#I'll draw it out.







