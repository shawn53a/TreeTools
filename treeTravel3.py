'''
Shawn Arreguin
3/19/26

Trying to figure out how to store the information in the tree
God, I wish I would just comment my fucking code.

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
        for x in BigList:
            travel(x)
    
    
            


#print(travel(tree))

class Node:
    
    children=[]
    allTips=[]
    node=""
    IntLabel=""
    allNodes=[]

    def __init__(self, node):
        self.node=node
        try:
            self.children, self.IntLabel=self.get_children()
        except TypeError:
            self.children=None
            self.IntLabel=None

    def get_children(self):

        return travel(self.node)
        
    
    def get_tips(self):
        
        if len(self.children) != 0:
            for x in self.children:
                
                tmp=Node(x)
                
                if tmp.children == None:
                    self.allTips.append(x)
                else:
                    tmp.get_tips()

    def get_allNodes(self):
        if len(self.children) != 0:
            for x in self.children:
                tmp=Node(x)
                if tmp.children == None:
                    pass
                else:
                    self.allNodes.append(x)
                    tmp.get_allNodes()

a=Node(tree)
#print(a.node)

a.get_children()
a.get_tips()
a.get_allNodes()
#print(a.IntLabel)
#print(a.children)
print(len(a.allTips))

for x in a.allTips:
    x=x.split(":")
    x=x[0].split("_")
    print(x[0],x[1],x[-1])
#print(a.allNodes)

