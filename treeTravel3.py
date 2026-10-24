'''
Shawn Arreguin
3/19/26

Last updated: 10/24/26
Next update needed: create a main statement

'''

import sys

file=open(sys.argv[1],"r")

tree=file.readline().strip()

#tree="A"


def justDaTip(node):
	return node

def travel(tree):
    c=0
    BigList=[]
    SmallStr=""
    #print("Initial:",tree)
    for x in tree:
        if (x =="," and c<2):
            BigList.append(SmallStr)
            SmallStr=""
        elif x == "(":
            c+=1
            if c>1:
                SmallStr+=x
        elif x == ")" and c==1:
            BigList.append(SmallStr)
            SmallStr=""
            c-=1
        elif x == ")":
            c-=1
            if c>=1:
                SmallStr+=x
        else:
            SmallStr+=x
    #print("Int:",SmallStr)
    if len(BigList)<1:
        pass
        #print("TIP:",tree,'\n')
        #Here is where I assign tip status and set children to BigList (which should be empty)
    else:
        #Here is where I assign children (set children to BigList)
        #print("children:",BigList,'\n')
        return BigList, SmallStr
        #for x in BigList:
           # travel(x)

            


#print(travel(tree))

class Node:

    nDict={}
    



    def __init__(self, node, parent=None):
        self.node=node
        self.parent=parent

        self.children=None
        self.allTips=[]
        self.intLabel="" #store internal label (node info, e.g., BS or BL)
        self.allNodes=[]

        self.sister=[]
        self.taxaName=None
        self.branchLength=None
        self.newName=[]


        try:
            self.children, self.intLabel=self.get_children()
        except TypeError:
            self.children=None
            self.intLabel=None

    def get_children(self):

        return travel(self.node)
        
    
    def get_tips(self):
        '''
        Find all tips. Lowkey sucked ass to make. Need to assign the tips all the way up.
        '''

        
        if self.children != None:

            for x in self.children:

                tmp=Node(x)
                
                if tmp.children == None:
                    print(x)
                    self.allTips.append(x) #Depending on where you are in the tree strucutre, self is going to be either tmp or it is going to be the original Node.
                    
                else:
                    tmp.get_tips() #at this point, self now becomes tmp.

                self.allTips.extend(tmp.allTips) #If self from the first comment was tmp, then we need to keep bringing alltips up through the ranks until it reaches the top.

        

    def get_allNodes(self):
        '''
        Conceptually, this is the same as get_tips, but you appending at a different point.
        '''

        if self.children != None:

            for x in self.children:

                tmp=Node(x)

                if tmp.children == None:
                    pass

                else:
                    self.allNodes.append(x)
                    tmp.get_allNodes()

                self.allNodes.extend(tmp.allNodes)

    

    def get_Sister(self):
        '''
        Only work if you have a parent
        '''

        tmp=Node(self.parent) #to find your sister, you must know your parents children

        for x in tmp.children:
            if self.node == x: #the sister(s) will be the children of the parent that are not itself
                pass
            else:
                self.sister.append(x) 



    def generateNode(self):
        '''
        Generate node objects from daughters
        '''

        if self.children != None:

            nodeList=[]

            for x in self.children:

                nodeList.append(Node(x,self.node))

            return nodeList




    def get_tip_features(self):
        '''
        Main purpose is to isolate features of the tip (species name, branch length)
        Specifically for the tip
        '''

        if self.children != None:
            return "This is for tips ONLY!"

        else:

            tmp=self.node.split(':')
            tipName=tmp[0]
            tipBL=tmp[1]

            self.branchLength=tipBL


            if tipName[-1]=="W": #This is pretty specific to my current project and would need to change for other shit.
                self.taxaName=tipName
            elif "_" in tipName:
                tipName=tipName.split("_")
                final=" ".join(tipName[:2])
                self.taxaName=final
            else:
                self.taxaName=tipName



    def change_Tip_Names(self):

        '''
        Change tip names to just species name and add a number to them if there are duplicates. Handy for gene trees.
        Conceptually pretty similar to the get_tips() function
        '''
        
        if self.children != None:
            
            
            for x in self.children:

                

                tmp=Node(x)

                
                if tmp.children == None:
                    tmp.get_tip_features()


                    ch=tmp.taxaName

                    if ch in self.nDict:
                        self.nDict[ch]+=1
                        ch=ch+str(self.nDict[ch])
                    else:
                        self.nDict[ch]=1

                    ch=ch+":"+tmp.branchLength

                    tmp.node=ch
                    self.newName.append(tmp.node)
                    #print("Self after if",self.node)


                else:
                    tmp.change_Tip_Names() #at this point, self now becomes tmp.
                    tmp.intLabel=")"+tmp.intLabel
                    tmp.newName[0]="("+tmp.newName[0]
                    tmp.newName[-1]=tmp.newName[-1]+tmp.intLabel #with this plus the last two lines, I am creating the new node name
                    self.newName.extend(tmp.newName) # adding the new node name created above
                    
                    #print(self.newName)
                    #print("Self after else",self.node)

            


        










#a=Node(tree)
#print(a.node)
#print(a.nodeInfo())
#print(a.node)

#a.get_children()
#a.get_tips()
#a.get_allNodes()
#print(a.IntLabel)
#print(a.children)
#print(a.allTips)

# for x in a.allTips:
#     x=x.split(":")
#     x=x[0].split("_")
#     print(x[0],x[1],x[-1])
#print(a.allNodes)






