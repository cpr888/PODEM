from mygraph import G
from operator import itemgetter 
import gates_lib
D_fronteir_list=[]
#-------------Funtion to initialise the controllability and Observability of thet nodes
def Initialising() :
	global G 
	for node in G.nodes(data=True):
		if( node[1]['type']!= 'input' and node[1]['cc0'] == 1 and node[1]['cc1'] == 1):
			Controllability_init(node[0])
	print "********************************************initialised_controllability**************************"	
	for node in G.nodes(data=True):
		if (node[1]['type']!='check'):
			flag = 0
#			print "inside Observability", node
			for incoming_edge in G.in_edges(node[0]):
				if G.edges[incoming_edge]['CO'] == 'x':
					flag = 1
			if flag==1:
				Observability_init(node[0])
	print "********************************************Observability_Initialised**************************"	

def Controllability_init(node):
	global G
#	print node, "in controllability_node"
   	for incoming in G.predecessors(node):
		if (G.node[incoming]['cc0'] == 1 and G.node[incoming]['cc1'] == 1 and G.node[incoming]['type'] != 'input'):
			Controllability_init(incoming)
   	l0=[]
   	l1=[]
   	for predecessors in G.predecessors(node):
   		l0.append(G.node[predecessors]['cc0'])
   		l1.append(G.node[predecessors]['cc1'])
   	#print G.node[node]['type']
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
    #	print (l0)
    #	print (node)


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
		#			predecessorCC0_list=[]
					predecessorCC1_list=[]
					for other_incoming_edge in G.in_edges(node):

						if other_incoming_edge!= incoming_edge :
		#					print other_incoming_edge,incoming_edge,"test"
		#					predecessorCC0_list.append(G.node[other_incoming_edge[0]]['cc0'])	 
							predecessorCC1_list.append(G.node[other_incoming_edge[0]]['cc1'])
		#			print node
		#			print successorsC0_list[0] 
		#			print sum(predecessorCC1_list) 	
					G.edges[incoming_edge]['CO']=successorsC0_list[0] + sum(predecessorCC1_list) +1	


			elif G.node[node]['gate_type'] =='or' or G.node[node]['gate_type']=='nor':
				
				for incoming_edge in G.in_edges(node):
					predecessorCC0_list=[]
		#			predecessorCC1_list=[]
					for other_incoming_edge in G.in_edges(node):
						if other_incoming_edge!= incoming_edge :
							predecessorCC0_list.append(G.node[other_incoming_edge[0]]['cc0'])	 
		#					predecessorCC1_list.append(G.node[other_incoming_edge[0]]['cc1'])

					G.edges[incoming_edge]['CO']=successorsC0_list[0] + sum(predecessorCC0_list) +1	

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


def primary_input():
	PIedge_list= []
	
	for item in G.nodes(data=True):
		
		if(item[1]['type']=='input'):
			list_outedge =list(G.out_edges(nbunch=item[0], data=False))	
			PIedge_list.append(list_outedge[0])
	return PIedge_list
	
def primary_output():
	POedge_list= []
	for item in G.nodes(data=True):
		if(item[1]['type']=='output'):
			list_outedge =list(G.in_edges(nbunch=item[0], data=False))	
			POedge_list.append(list_outedge[0])
	return POedge_list

#Finding the Faulty edges
def faulty_edg():								
	for item in G.edges(data=True):
		if(item[2]['fault']=='sa1' ):
			return [item[0],item[1],'sa1','0']				
		elif(item[2]['fault']=='sa0'):
			return [item[0],item[1],'sa0','1']

	
#def Backtrace(edge,value):

def get_setting(gate,val):
	global G 
	if (G.node[gate]['gate_type']=='and' and val=='0') or (G.node[gate]['gate_type']=='or' and val=='1') or (G.node[gate]['gate_type']=='nand' and val=='1') or (G.node[gate]['gate_type']=='nor' and val=='0'):
		return 1
		# setting 1 means only one value have to be controlled
	else:
		return 0
		# setting 0 means all the inputs have to be controlled


def Backtrace(input_list, vs):
	global G
	print "input list in bactrace =",input_list,"vs",vs	
	flag=1
	setting=0
	v=vs
	v_f='x'
	# this flag is used in the future where we have ti decide which valaue to check
	if v=='0':
		flag='cc0'
	else:
		flag='cc1'
	updated_input_list=input_list
	s=input_list[0]
	if G.node[s]['type']=='fanout':
		for incoming in G.predecessors(s):
			s=incoming
			temp =(s,input_list[0])
			updated_input_list=temp
			print "updated input list after checking fanout",updated_input_list,vs		
	
	print "node type= " , G.node[s]['type']
	if G.node[s]['type']=='input':
		return updated_input_list,vs
	elif G.node[s]['type']!='input':
		if G.node[s]['gate_type']=='nand' or G.node[s]['gate_type']=='nor' or G.node[s]['gate_type']=='not':
			print "inside the value change"
			if v=='1':
				v='0'
			elif v=='0':
				v='1'
		setting=get_setting(s,v)
		max_ctrl_val=0
		min_ctrl_val=50
		print "input list in bactrace =",input_list,"vs",vs	
		if setting==1:			#all inpiuts are to be controlled
			print " seeting = 1"
			for in_edge in G.in_edges(s):
				if G.node[in_edge[0]][flag] >= max_ctrl_val and G.edges[in_edge]['value_non_fault']=='x':	#if you want to find the max CC0
					max_ctrl_val=G.node[in_edge[0]][flag]
					nxt_backtrack_edge = in_edge
					if G.node[nxt_backtrack_edge[0]]['type']=='fanout':
						for var in G.in_edges(nxt_backtrack_edge[0]):
							nxt_backtrack_edge=var
			if G.node[nxt_backtrack_edge[0]]['type'] == 'input' :
				return (nxt_backtrack_edge,v)	
			else:
				if (G.node[nxt_backtrack_edge[0]]['gate_type'] == 'nand' or G.node[nxt_backtrack_edge[0]]['gate_type'] == 'nor' or G.node[nxt_backtrack_edge[0]]['gate_type'] == 'not'):
					print "in here"
					pi,v_f=Backtrace(nxt_backtrack_edge,v)
		elif setting==0:
			print " seeting = 0"
			for in_edge in G.in_edges(s):
				if G.node[in_edge[0]][flag] <= min_ctrl_val and G.edges[in_edge]['value_non_fault']=='x':	#if you want to find the max CC0
					min_ctrl_val=G.node[in_edge[0]][flag]
					print "in_edge,ctrl",in_edge ,min_ctrl_val
					nxt_backtrack_edge = in_edge
					if G.node[nxt_backtrack_edge[0]]['type']=='fanout':
						for var in G.in_edges(nxt_backtrack_edge[0]):
							nxt_backtrack_edge=var
					print "in_edge,nxt_backtrack_edge,v",in_edge ,nxt_backtrack_edge,v
			if G.node[nxt_backtrack_edge[0]]['type'] == 'input' :
				print "gonna return this as its input node"
				return nxt_backtrack_edge,v
			else:
				if (G.node[nxt_backtrack_edge[0]]['gate_type'] == 'nand' or G.node[nxt_backtrack_edge[0]]['gate_type'] == 'nor' or G.node[nxt_backtrack_edge[0]]['gate_type'] == 'not'):
					print "in here to Backtrace"
					pi,v_f=Backtrace(nxt_backtrack_edge,v)
	
		return pi,v_f


def Forward_Implication(node1,node2):
	global G
	print "\n \n \n node1",node1,"node2",node2
	list_outedges =list(G.out_edges(nbunch=node2, data=False))				
	list_inedges =list(G.in_edges(nbunch=node2, data=False))
	print "faulty_edge_list[:2]",faulty_edge_list[:2]
			
	
	if(G.nodes[node2]['type']=='fanout'):

		print "faulty_edge_list[:2]",faulty_edge_list[:2]
		print "G[node1][node2]['value_faulty']",G[node1][node2]['value_faulty']
		for i in range(len(list_outedges)):
		
			G.edges[list_outedges[i]]['value_non_fault']  = G[node1][node2]['value_non_fault']
			if(faulty_edge_list[0]!=list_outedges[i][0] or faulty_edge_list[1]!=list_outedges[i][1]):
				G.edges[list_outedges[i]]['value_faulty']  = G[node1][node2]['value_faulty']
			
			next_node1		=list_outedges[i][0]
			next_node2		=list_outedges[i][1]
			print "new_node1 new_node2",next_node1,next_node2,G.edges[list_outedges[i]]['value_faulty'] 	
			if(G.nodes[next_node2]['type']=='gate' or G.nodes[next_node2]['type']=='fanout'):
				Forward_Implication(next_node1,next_node2)
			
			#next_node1	= node1
			#next_node2	= node2
	elif(G.nodes[node2]['type']=='gate'):
		list_input_non_faulty =[]
		list_input_faulty	  =[]
		print G.nodes[node2]['gate_type'],node2	
		for i in range(len(list_inedges)):
			list_input_non_faulty.append(G.edges[list_inedges[i]]['value_non_fault'])
			list_input_faulty.append(G.edges[list_inedges[i]]['value_faulty'])
		print "fault list",list_input_faulty 
		print "nonfault list",list_input_non_faulty
		
		if(G.nodes[node2]['gate_type']=='and'):
			output_non_faulty = gates_lib.AND_gate(list_input_non_faulty)
			output_faulty	  = gates_lib.AND_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='or'):
			output_non_faulty =	gates_lib.OR_gate(list_input_non_faulty)
			output_faulty	  =	gates_lib.OR_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='nand'):
			output_non_faulty =	gates_lib.NAND_gate(list_input_non_faulty)
			output_faulty	  = gates_lib.NAND_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='nor'):
			output_non_faulty =	gates_lib.NOR_gate(list_input_non_faulty)
			output_faulty      =gates_lib.NOR_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='xor'):
			output_non_faulty =	gates_lib.XOR_gate(list_input_non_faulty)
			output_faulty      =gates_lib.XOR_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='xnor'):
			output_non_faulty =	gates_lib.XNOR_gate(list_input_non_faulty)
			output_faulty      =gates_lib.XNOR_gate(list_input_faulty)
		elif(G.nodes[node2]['gate_type']=='not'):
			output_non_faulty =	gates_lib.NOT_gate(list_input_non_faulty[0])
			output_faulty	  = gates_lib.NOT_gate(list_input_faulty[0])
			#print "OUTPUT",output_non_faulty
		#Assign the value_non_fault to the output_non_faulty nodes
		print output_non_faulty,"non_faulty)output @",list_outedges[0]
		G.edges[list_outedges[0]]['value_non_fault'] = output_non_faulty 
				
		print "list_outedge",list_outedges[0] ,"and the faulty_edge_list=",faulty_edge_list	
		print "list_outedge[0][0]",list_outedges[0][0] ,"and the faulty_edge_list[0]=",faulty_edge_list[0]

		print "list_outedge[0][1]",list_outedges[0][1] ,"and the faulty_edge_list[1]=",faulty_edge_list[1]	
		print 

		if(faulty_edge_list[0] !=list_outedges[0][0] or faulty_edge_list[1] !=list_outedges[0][1]): 		#in case of the Gates, the output egdes will have only one element(tuple)
			G.edges[list_outedges[0]]['value_faulty'] = output_faulty 
			print output_faulty,"faulty_output @",list_outedges[0]
		
			
		next_node1 =list(G.out_edges(nbunch=node2, data=False))[0][0]
		next_node2 =list(G.out_edges(nbunch=node2, data=False))[0][1]
		#print "node1 node2",node1,node2
		if(G.nodes[node2]['type']!='output'):		#Check whether Fault Propagated to Primary output_non_faulty
			Forward_Implication(next_node1,next_node2)




def Objective():
		global G
		global faulty_edge_list
		print faulty_edge_list,"faulty list"
		global D_fronteir_list
#		print  "D_fronteir_list",D_fronteir_list
		
		if(G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']=='x'):	#Sensitize the fault
			if(faulty_edge_list[2]=='sa1'):									# if sa1 then it should have non faulty value = 0
#				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']='0'
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_faulty']   ='1'
				value = '0'
				
				
			elif(faulty_edge_list[2]=='sa0'):								# if sa0 then it should have non faulty value = 1
#				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']='1'
				G[faulty_edge_list[0]][faulty_edge_list[1]]['value_faulty']   ='0'
				value = '1'
			
			print "here"
#			D_fronteir_list.append((faulty_edge_list[0],faulty_edge_list[1]))
#			print  "D_fronteir_list",D_fronteir_list
			
			return  faulty_edge_list[0],faulty_edge_list[1],value
			
											#Enable the propagation ofthe fault by assigning them non controling values
#		D_fronteir_list= D_fronteir()
		print "sort_D_fronteir"
		print D_fronteir_list
		D_fronteir_list_CO = {}
	#	print  G.edges.keys()
		for i in D_fronteir_list:
			for j in G.edges.keys():
				if(i==j):
					print "here in loop"
					print i , j
					D_fronteir_list_CO[i] = G.edges[j]['CO']
##for testing#
#		D_fronteir_list_CO[('fan1','N4')] = 8
##end of the statement for the testing#
		print "D_fronteir_list_CO" 	, D_fronteir_list_CO
		
		D_fronteir_list_CO_sorted = sorted(D_fronteir_list_CO.items(), key=itemgetter(1))
	
		print "D_fronteir_list_CO_sorted",D_fronteir_list_CO_sorted
		print D_fronteir_list_CO_sorted[0][0][1]
		gate_ip_edge,value = assign_undefined_ip(D_fronteir_list_CO_sorted[0][0][0])
	
		return gate_ip_edge[0],gate_ip_edge[1],value



def assign_undefined_ip(node_D_fronteir):
		#Assigning a non-controlling value to the gate
	print "-------------------------------------assign_undefined_ip------------------------------------------"
	print "node_D_fronteir",node_D_fronteir 
	global G
	print "NODES" , G.nodes(data=True)
	gate_type =G.nodes[node_D_fronteir]['gate_type']
	gate_ip_edge = list(G.in_edges(nbunch=node_D_fronteir, data=False))
	#new_D_fronteir_edge=list(list(G.out_edges(nbunch=node_D_fronteir, data=False))[0])
	if (gate_type =='not'):
		#print "gate_ip_edge",list(gate_ip_edge[0])
		return list(gate_ip_edge[0])
	else:
		if(gate_type=='and' or  gate_type=='nand'):
			control_val =0
		elif(gate_type=='or' or  gate_type=='nor'):
			control_val =1
		for i in range(len(gate_ip_edge)):
				if(G.edges[gate_ip_edge[i]]['value_non_fault']=='x' or G.edges[gate_ip_edge[i]]['value_faulty']=='x'):
					if (gate_type == 'xor' or gate_type == 'xnor') and (G.node[gate_ip_edge[i][0]]['cc0'] < G.edges[gate_ip_edge[i]][0]['cc1']):
       						control_val = 1
   					else:
       						control_val = 0
					return gate_ip_edge[i],str(int(not control_val))
	return 0



		


def D_fronteir():

	global faulty_edge_list
	D_fronteir_li	=[]


	if(G[faulty_edge_list[0]][faulty_edge_list[1]]['value_non_fault']=='x'):	#Sensitize the fault
		print "faulty edge is added to D_fronteir_list"
		D_fronteir_li.append((faulty_edge_list[0],faulty_edge_list[1]))

	for i in G.nodes:
#		print i
		flag1 =False
		flag2 =False

		if(G.nodes[i]['type']=='gate'):
			#print "ioaefjpeiofljpowef'''''"
			gate_op_edge = list(G.out_edges(nbunch=i, data=False))
			gate_ip_edge = list(G.in_edges(nbunch=i, data=False))
			
			if(G.edges[gate_op_edge[0]]['value_non_fault']=='x' or G.edges[gate_op_edge[0]]['value_faulty']=='x'):		#Output is 'x'
				for j in gate_ip_edge:
					if(G.edges[j]['value_non_fault']=='1' and G.edges[j]['value_faulty'] =='0') or (G.edges[j]['value_non_fault']=='0' and G.edges[j]['value_faulty'] =='1'): #Input is D or D_bar check
						flag1=True	
						print " d or d_bar in nodes:",j
					if(G.edges[j]['value_non_fault']=='x' or G.edges[j]['value_faulty']=='x'):							#one of the Other Inputs is 'x'
						flag2= True
			
			if(flag1==True and flag2 ==True):
							print "D_fronteir in the_ ", j
							D_fronteir_li.insert(0,gate_op_edge[0])
							print "D_fronteir in the_appened case ", D_fronteir_li
			
	
	return D_fronteir_li


print "\n\nEDGES:\n\n \n"	
for edge in G.edges(data=True):
	#print edge
	print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']



def error_at_PO():
		global G
		global PO_edge_list
		print "check if D/D_bar is at output"
		for i in PO_edge_list:
			if(G.edges[i]['value_non_fault']!='x' and G.edges[i]['value_faulty']!='x' and G.edges[i]['value_non_fault']!=G.edges[i]['value_faulty'] ):
				print "D/D_bar is at output",i
				return True

		return False 

def assign_value_to_PI(PI_edge, value):
		global G
		global faulty_edge_list
		G[PI_edge[0]][PI_edge[1]]['value_non_fault']= value
		if(faulty_edge_list[0]!=PI_edge[0] or faulty_edge_list[1]!=PI_edge[1]):			#assign the true value in faulty, only if that node is non faulty
			G[PI_edge[0]][PI_edge[1]]['value_faulty']= value

		implications_stack.append((PI_edge,value))

def backtrack():
	global implications_stack
	#print li[-1][0],li[-2][0]
	while (implications_stack[-1][0]==implications_stack[-2][0]):
		#print "in loop:",li[-1][0],li[-2][0]
		implications_stack.pop(-1)
		implications_stack.pop(-1)
		if (len(implications_stack)==0):
			print "No test casepossible"
			return
		elif (len(implications_stack)<2):
			n=implications_stack[-1][0]
			v=implications_stack[-1][1]
			if v=='1':
				vf='0'
			elif v=='0':
				vf='1'
			implications_stack.pop(-1)
			print implications_stack
			implications_stack.append((n,vf))
			print implications_stack
			return implications_stack
	n1=implications_stack[-1][0]
	v1=implications_stack[-1][1]
	if v1=='1':
		vf1='0'
	elif v1=='0':
		vf1='1'
	implications_stack.pop(-1)
	print "implications_stack",implications_stack
	implications_stack.append((n1,vf1))
	print "n1,vf1",n1,vf1
	return n1,vf1		


def main_PODEM():
		global G
		global D_fronteir_list
		global PO_edge_list
		global implications_stack
		global count 
		pi=[]
		#count = count+1
		count_limit=0
		while (not (error_at_PO()) and count_limit<10 ):
			count_limit=count_limit+1
			print "while loop"
			print "---------------------------EDGES while entering the PODEM whileloop------------------------------------------------------------------"
			for edge in G.edges(data=True):
				#print edge
			
				print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']

			D_fronteir_list= D_fronteir()
			print "count=",count ,"length  of D_fronteir_list= ",len(D_fronteir_list)
			if len(D_fronteir_list)!=0: ###############removed this portion,needs to check########s##### or count==0 : 
				count = count+1
				print "count=",count
				print "------------------------------------------------Objective round",count," --------------------------"
				node1,node2,vs=Objective()
				print "D_fronteir_list",D_fronteir_list
				print "length  of D_fronteir_list= ",len(D_fronteir_list)
				print "----------------------------------------Objective round",count," DONE--------------------------"
				print "node1,node2,vs=",node1,node2,vs
				print "------------------------------------------------BACKTRACE round",count," --------------------------"
				pi,v=Backtrace((node1,node2),vs)
				
				print "------------------------------------------------Backtrace round",count," DONE--------------------------"
				print pi,v ,"Backtraced values"
				print "------------------------------------------------Value assignment round",count," --------------------------"
				
				assign_value_to_PI(pi,v);
				print "---------------------------EDGES after assignment------------------------------------------------------------------"
				for edge in G.edges(data=True):
				#print edge
			
						print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']

				print "------------------------------------------------Forward_Implication round",count," --------------------------"
				
				Forward_Implication(pi[0],pi[1])
				print "---------------------------EDGES after implication------------------------------------------------------------------"
				for edge in G.edges(data=True):
				#print edge
			
						print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']

				if main_PODEM():
					return True
				result = Backtrack()  # Backtrack can return new PI assignmnet or an empty list
				if not result:  # implications list has been exhausted
					return False
				else:
					pi = result[:2]
					v = result[2]
					print "pi,v after backtrack =",pi,v
					print "------------------------------------------------Value assignment round",count," --------------------------"
					assign_value_to_PI(pi,v);
					print "------------------------------------------------Forward_Implication round",count," --------------------------"

					Forward_Implication(pi[0],pi[1])

				if main_PODEM():
					return True
				print "----------as the current pi=",pi,"assignment of either 0 or 1 is not helpful, we are backtracking again"

				v='x'

				assign_value_to_PI(pi,v);

				Forward_Implication(pi[0],pi[1])
				return False
			elif not implications_stack:
				return False
	#        else:
	#            result = Backtrack(G, implications)
		return True

		
faulty_edge_init =['N23','output2','sa0']  ## INPUT FROM THE USER 
G.add_edge(faulty_edge_init[0],faulty_edge_init[1], value_non_fault='x',value_faulty='x',fault=faulty_edge_init[2],CO='x')


faulty_edge_list=faulty_edg()
print "--------------------------finding faulty node ------------------------------------------------"
print "fault==", faulty_edge_list
count = 0;
PI_edge_list=primary_input();
PO_edge_list=primary_output();
implications_stack=[]

main_PODEM()
print "end of main_PODEM"
print implications_stack

#print "------------------------------------------------Objective round1: -------------------------------"
#node1,node2,vs=Objective()	
#print "--------------------------finding faulty node ------------------------------------------------"
#print "fault==", faulty_edge_list
#print "node1,node2,vs=",node1,node2,vs
#pi,v=Backtrace((node1,node2),vs)#,faulty_edge_list[3])
#print "------------------------------------------------Backtraced round1 DONE--------------------------"
#print pi,v ,"Batraced values"
###G[pi[0]][pi[1]]['value_non_fault']= v
###G[pi[0]][pi[1]]['value_faulty']= v
###G['N6']['N11']['value_non_fault']='0'
###G['N6']['N11']['value_faulty']='0'
###Forward_Implication(pi[0],pi[1])
#G[pi[0]][pi[1]]['value_non_fault']= v
#G[pi[0]][pi[1]]['value_faulty']= v
#Forward_Implication(pi[0],pi[1])
#
#print "\n\nEDGES:\n\n \n"	
#
##print list(G.edges.keys())

#
##print "\n\nEDGES:\n\n \n"	
#for edge in G.edges(data=True):
#	#print edge
#
#	print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']

#
#print "------------------------------------------------Objective round2: --------------------------"
#
#node1,node2,vs=Objective()	
#print "node1,node2,vs=",node1,node2,vs
#print "------------------------------------------------Backtraced round2 start--------------------------"
#pi,v=Backtrace((node1,node2),vs)#,faulty_edge_list[3])
#print "------------------------------------------------Backtraced round2 DONE--------------------------"
#print pi,v ,"Batraced values"
###G[pi[0]][pi[1]]['value_non_fault']= v
###G[pi[0]][pi[1]]['value_faulty']= v
###G['N6']['N11']['value_non_fault']='0'
###G['N6']['N11']['value_faulty']='0'
###Forward_Implication(pi[0],pi[1])
#G[pi[0]][pi[1]]['value_non_fault']= v
#G[pi[0]][pi[1]]['value_faulty']= v
#Forward_Implication(pi[0],pi[1])
#
#print "\n\nEDGES:\n\n \n"	
#
##print list(G.edges.keys())

#
##print "\n\nEDGES:\n\n \n"	
#for edge in G.edges(data=True):
#	#print edge
#
#	print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']

#
#print "------------------------------------------------Objective round3: --------------------------"
#
#node1,node2,vs=Objective()	
#print "node1,node2,vs=",node1,node2,vs
#print "------------------------------------------------Backtraced round3 start--------------------------"
#pi,v=Backtrace((node1,node2),vs)#,faulty_edge_list[3])
#print "------------------------------------------------Backtraced round3 DONE--------------------------"
#print pi,v ,"Batraced values"
###G[pi[0]][pi[1]]['value_non_fault']= v
###G[pi[0]][pi[1]]['value_faulty']= v
###G['N6']['N11']['value_non_fault']='0'
###G['N6']['N11']['value_faulty']='0'
###Forward_Implication(pi[0],pi[1])
#G[pi[0]][pi[1]]['value_non_fault']= v
#G[pi[0]][pi[1]]['value_faulty']= v
#Forward_Implication(pi[0],pi[1])
#
#print "\n\nEDGES:\n\n \n"	
#
##print list(G.edges.keys())

#
##print "\n\nEDGES:\n\n \n"	
#for edge in G.edges(data=True):
#	#print edge
#
#	print edge[0],edge[1],"not_faulty",edge[2]['value_non_fault'],"faulty",edge[2]['value_faulty']
