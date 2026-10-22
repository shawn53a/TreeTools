'''
Shawn Arreguin
3/26/26

NJ Program functions
'''

import sys



def ReadsFasta(file):
	'''
	Read in our fasta file and build a dictionary with it.
	'''

	seqDic={}

	for line in file:

		line=line.strip("\n")

		if ">" in line:
			n=line.strip(">")
			seqDic[n]=""
		else:
			seqDic[n]+=line

	return seqDic



def MyNames(file):
	'''
	Just gives sequence names and number of them
	'''

	seqDic = ReadsFasta(file)
	#count=len(seqDic)

	names=[]
	for x in seqDic:
		names.append(x)

	return names


def csvDist(file):
	'''
	Reads in a premade distance matrix that is in CSV format. Saves the Names and Values.
	Here we assume that there are row headers and column headers and that they're in the same order.
	'''

	file.readline()

	Names=[]
	BigList=[]
	for line in file:
		smol=[]
		line=line.strip()
		line=line.split(",")
		for x in range(len(line)):
			if x == 0:
				Names.append(line[x])
			else:
				smol.append(line[x])

		BigList.append(smol)

	matrixPrinter(Names,BigList)
	return Names, BigList


def tsvDist(file):
	'''
	Reads in a premade distance matrix that is in TSV format. Saves the Names and Values.
	Here we assume that there are row headers and column headers and that they're in the same order.
	'''

	file.readline()

	Names=[]
	BigList=[]
	for line in file:
		smol=[]
		line=line.strip()
		line=line.split("\t")
		for x in range(len(line)):
			if x == 0:
				Names.append(line[x])
			else:
				smol.append(line[x])
				
		BigList.append(smol)

	matrixPrinter(Names,BigList)
	return Names, BigList





def distMatrix(file):
	'''
	Make a distance matrix of the sequences in the fasta file.
	Simple Hamming distance.
	'''

	seqDic=ReadsFasta(file)

	BigList=[]
	Names=[]

	i=-1

	#Compares each element in fasta. 
	#checks differences and appends to a list and makes a matrix at end
	#What the fuck is 'i' and 'j' here?
	for name in seqDic:
		SmlList=[]
		Names.append(name)
		i+=1
		j=-1
		for otherName in seqDic:
			j+=1

			dif=0
			for nuc in range(len(seqDic[name])):
				if seqDic[name][nuc] != seqDic[otherName][nuc]:
					dif+=1
			#print(seqDic[name],seqDic[otherName],str(dif))

			SmlList.append(str(dif))
			#print(name, otherName)


		BigList.append(SmlList)

	#print(BigList)

	matrixPrinter(Names,BigList)

	return Names, BigList



def matrixPrinter(Names,AA):
	'''
	Print matrix
	'''

	print("\t"+"\t".join(Names))
	for i in range(len(AA)):
		print(Names[i]+"\t"+"\t".join(AA[i]))



def qMatrix(Names, BigList):
	'''
	Make a qMatrix given your distance matrix
	qMatrix = (n-2)*d(i,j)- SUM[all distances of i] - SUM[all distances of j]
	'''

	#print(Names, BigList)

	numb_taxa=len(BigList)

	q=[]
	min_val=0
	best_i=""
	best_j=""

	for i in range(len(BigList)):
		smol=[]
		for j in range(len(BigList)):
			#print(i,j,BigList[i][j],"shit")

			#print(Names[i],Names[j])

			#find every distance pair between i and other members of the matrix. sum them all up.
			row_v=0
			#print("row")
			#this kinda mind fucks me. Instead of going down the row to get the value,
			#we go down the column that holds the exact same values as the row. We can sswitch
			#row and i and get the same values, which makes sense, but its also fucked.
			#cuz A's column and row are identical, which makes sense cuz its a matrix.
			for row in range(len(BigList[i])):
				row_v+=float(BigList[row][i])
				#print(BigList[row][i],row,i)

			
			#find every distance pair between j and other members of the matrix. sum them all up.
			col_v=0
			#print("col")
			#see above row message cuz its essentially the same. Kinda mind fucks me
			for col in range(len(BigList)):
				col_v+=float(BigList[col][j])
				#print(BigList[col][j],col,j)

			
			#calculate new value in qMatrix
			if i==j:
				new_Val=0
			else:
				new_Val=(numb_taxa-2)*float(BigList[i][j]) - col_v - row_v
				#print("here",numb_taxa-2,BigList[i][j],col_v,row_v)
				if min_val > new_Val:
					min_val=new_Val
					best_i=i
					best_j=j
					best_row=row_v
					best_col=col_v

			smol.append(str(new_Val))

		q.append(smol)

	matrixPrinter(Names, q)
	print(min_val, best_i, best_j, Names[best_i],Names[best_j])
	return q, min_val, best_i, best_j, best_row, best_col


def branchEst2(BigList, best_i, best_j, best_row, best_col):
	n=len(BigList)

	branchA=(0.5*float(BigList[best_i][best_j]))+(1/(2*(n-2)))*(best_row - best_col) #sum of distances between a and all other nodes - sum of distances between b and all other nodes
	branchB=float(BigList[best_i][best_j])-branchA

	return branchA, branchB


def branchEst3(BigList):
	n=len(BigList)

	BigList0=[float(x) for x in BigList[0]]
	sum0 = sum(BigList0)
	BigList1=[float(x) for x in BigList[1]]
	sum1 = sum(BigList1)

	branchA=float(0.5*float(BigList[0][1])+(1/(2*(n-2)))*(sum0-sum1))
	branchB=float(BigList[0][1])-branchA
	branchC=float(BigList[0][2])-branchA

	return branchA, branchB, branchC



def updateDatDistancM(Names, BigList, q, best_i, best_j):
	
	#You need to original distance matrix. You must use this to create a new distance matrix
	#that will be n-1 smaller. You will then feed this new distance matrix to the q matric maker.


	NewBig=[]
	NewNames=[]

	for i in range(len(Names)+1):
		smolList=[]
		
		for j in range(len(Names)+1):
			if i == 0 and j == 0:
				smolList.append("0")
				NewNames.append(Names[best_i]+Names[best_j]) #or call this N1 or NJ1 and we can continue to add a number to it as we progress
			elif i == 0 and j != 0:
				if j-1 == best_i or j-1 == best_j:
					pass
				else:
					#print(Names[i],Names[j-1])
					tmpD=0.5*(float(BigList[best_i][j-1])+float(BigList[best_j][j-1])-float(BigList[best_i][best_j]))
					smolList.append(str(tmpD))
					NewNames.append(Names[j-1])
			elif j == 0 and i != 0:
				if i-1 == best_i or i-1 == best_j:
					pass
				else:
					#print(Names[i-1],Names[j])
					tmpD=0.5*(float(BigList[best_i][i-1])+float(BigList[best_j][i-1])-float(BigList[best_i][best_j]))
					smolList.append(str(tmpD))
			elif i != 0 and j != 0:
				if (i-1 == best_i or i-1 == best_j) or (j-1 == best_i or j-1 == best_j):
					pass
				else:
					#print(Names[i-1],Names[j-1])
					smolList.append(BigList[i-1][j-1])
			else:
				pass
		
		
		if not smolList:
			pass
		else:
			NewBig.append(smolList)

	#print(NewNames)
	#print(NewBig)
	matrixPrinter(NewNames,NewBig)

	return NewNames, NewBig


if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("oh fuck, need a file or we have too many :(")
		sys.exit()

	file=open(sys.argv[1],"r")


	Names, BigList=distMatrix(file)

	q, min_val, best_i, best_j, branchA, branchB = qMatrix(Names, BigList)

	NewNames, NewBig = updateDatDistancM(Names, BigList, q, best_i, best_j)


	qMatrix(NewNames, NewBig)



#I have to think about how to incorporate tree traveler in this.




	




