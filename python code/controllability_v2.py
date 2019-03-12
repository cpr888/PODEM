""" this code receives input from mygraph.py. It will pass the 'G' """

import networkx as nx
from mygraph import G
#print(G.node)
#print(G.edges)
print "________________________________________________________________________________________________________________"
def get_controllability(G, node):
    #We will receive the node of which controllability has to be find out as the inout argument to this function.
    #this is a recursive function. We will first search node till the input. and start calculating the controllability.
    
        for incoming in G.predecessors(node):                   
            if G.node[incoming]['cc0'] == 1 and G.node[incoming]['cc1'] == 1 and G.node[incoming]['type'] != 'input':
                get_controllability(G, incoming)
    #Every time we will use a fresh list"""
        l0=[]
        l1=[]
    #To calculate controllability, we will require the controllability of previous node"""
        for predecessors in G.predecessors(node):
            l0.append(G.node[predecessors]['cc0'])
            l1.append(G.node[predecessors]['cc1'])
    #Fanouts and output nodes wont conntribute anything in the calculating controllability"""
        if G.node[node]['type'] == 'output' or G.node[node]['type'] == 'fanout' :
            G.node[node]['cc0'] = G.node[predecessors]['cc0']
            G.node[node]['cc1'] = G.node[predecessors]['cc1']
    #For other nodes we have to find which gate and depending on that we have to find controllability of current node
    #using the information of previous node which is saved in the list
        elif G.node[node]['gate_type'] == 'and':
            G.node[node]['cc0'] = min(l0) + 1
            G.node[node]['cc1'] = sum(l1) + 1

        elif G.node[node]['gate_type'] == 'nand':
            G.node[node]['cc0'] = sum(l1) + 1
            G.node[node]['cc1'] = min(l0) + 1

        elif G.node[node]['gate_type'] == 'or':
            G.node[node]['cc0'] = sum(l0) + 1
            G.node[node]['cc1'] = min(l1) + 1

        elif G.node[node]['gate_type'] == 'nor':
            G.node[node]['cc0'] = min(l1) + 1
            G.node[node]['cc1'] = sum(l0) + 1

        elif G.node[node]['gate_type'] == 'not':
            G.node[node]['cc0'] = l1[0] + 1
            G.node[node]['cc1'] = l0[0] + 1
        
def main():
    get_controllability(G,'N22')
    get_controllability(G,'N23')
    for node in G.node :
        print node ,"CC0=", G.node[node]['cc0'],"CC1=", G.node[node]['cc1']
main()    