from mygraph import G
#-------------Funtion to initialise the controllability and Observability of thet nodes
def Initialising() :
	global G 
	for node in G.nodes(data=True):
		if( node[1]['type']!= 'input' and node[1]['cc0'] == 1 and node[1]['cc1'] == 1):
			get_controllability(node[0])
	print "********************************************initialised_controllability**************************"	
	for node in G.nodes(data=True):
		if (node[1]['type']!='check'):
			flag = 0
			print "inside Observability", node
			for incoming_edge in G.in_edges(node[0]):
				if G.edges[incoming_edge]['CO'] == 'x':
					flag = 1
			if flag==1:
				Observability_init(node[0])
	print "********************************************Observability_Initialised**************************"	

def get_controllability(node):
	global G
	print node, "in controllability_node"
   	for incoming in G.predecessors(node):
		if (G.node[incoming]['cc0'] == 1 and G.node[incoming]['cc1'] == 1 and G.node[incoming]['type'] != 'input'):
			get_controllability(incoming)
   	l0=[]
   	l1=[]
   	for predecessors in G.predecessors(node):
   		l0.append(G.node[predecessors]['cc0'])
   		l1.append(G.node[predecessors]['cc1'])
   	print G.node[node]['type']
   	if G.node[node]['type'] == 'check':
   		return
   	if G.node[node]['type'] == 'output' or G.node[node]['type'] == 'fanout' :
   	   # for predecessors in G.predecessors(node):
   		G.node[node]['cc0'] = G.node[predecessors]['cc0']
   		G.node[node]['cc1'] = G.node[predecessors]['cc1']
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
      
         
      #G.node[node]['cc0'] = l0
      #G.node[node]['cc1'] = l1
      #print(G.node['G5']['cc0'])
      #print(G.node['G5']['cc1'])
    	print (l0)
    	print (node)


def Observability_init(node):
#	for outgoing in G.successors(node):
#		if  (G.[outgoing]['type']='output'):
#			return
	global G 
#	for edge in G.edges(data=True):
#		print edge[0],edge[1],edge[2]['CO']
	#print "###########################################################################################################"
	if G.node[node]['type'] == 'output' :
		for incoming_edge in G.in_edges(node):
		#		print "node = output ,so CO=0"
				G.edges[incoming_edge]['CO'] = 0;
	elif G.node[node]['type'] == 'input':
		for incoming_edge in G.in_edges(node):
			for outgoing_edge in G.out_edges(node):
				G.edges[incoming_edge]['CO']=G.edges[outgoing_edge]['CO']

	else:
		successorsC0_list=[]
		for outgoing_edge in G.out_edges(node):
			if (G.edges[outgoing_edge]['CO'] == 'x'):
		#	 	print "going in Observability_init(", outgoing_edge[1],")"
			 	Observability_init(outgoing_edge[1])			#out_egde will be list = [ (Start node,end node )]
		#	 	print "Finished in Observability_init(", outgoing_edge[1],")"
			
			successorsC0_list.append(G.edges[outgoing_edge]['CO'])

			 	

		if G.node[node]['type'] =='fanout':
			for stem in G.in_edges(node):
				G.edges[stem]['CO']= min(successorsC0_list)

		else:
			if G.node[node]['gate_type'] =='and' or G.node[node]['gate_type']=='nand':
				for incoming_edge in G.in_edges(node):
					predecessorCC0_list=[]
					predecessorCC1_list=[]
					for other_incoming_edge in G.in_edges(node):

						if other_incoming_edge!= incoming_edge :
		#					print other_incoming_edge,incoming_edge,"test"
							predecessorCC0_list.append(G.node[other_incoming_edge[0]]['cc0'])	 
							predecessorCC1_list.append(G.node[other_incoming_edge[0]]['cc1'])
					print node
					print successorsC0_list[0] 
					print sum(predecessorCC1_list) 	
					G.edges[incoming_edge]['CO']=successorsC0_list[0] + sum(predecessorCC1_list) +1	


			elif G.node[node]['gate_type'] =='or' or G.node[node]['gate_type']=='nor':
				
				for incoming_edge in G.in_edges(node):
					predecessorCC0_list=[]
					predecessorCC1_list=[]
					for other_incoming_edge in G.in_edges(node):
						if other_incoming_edge!= incoming_edge :
							predecessorCC0_list.append(G.node[other_incoming_edge[0]]['cc0'])	 
							predecessorCC1_list.append(G.node[other_incoming_edge[0]]['cc1'])

					G.edges[incoming_edge]['CO']=successorsC0_list[0] + sum(predecessorCC1_list) +1	

			elif G.node[node]['gate_type'] =='not': 
				for stem in G.in_edges(node):
					G.edges[stem]['CO']= successorsC0_list[0] + 1 

for outgoing_edge in G.out_edges('N11'):
	print outgoing_edge

#	print G.edges[outgoing_edge]['CO']

#for node in G.node(data=True):
#	print "main call:",node
#	print node[0]
#	Observability_init(node[0])
Initialising()
#print "NODES: \n", G.nodes(data=True),"\n \n"
print "\n\nNODES: \n"
for node in G.node(data=True):
	print node[0],"CC0=",node[1]['cc0'],"CC1=",node[1]['cc1']

print "\n\nEDGES:\n\n \n"	
for edge in G.edges(data=True):
	#print edge
	print edge[0],edge[1],"CO=",edge[2]['CO']
#	print node[0]
#print "EDGES:\n", G.edges(data=True) ,"\n \n"
