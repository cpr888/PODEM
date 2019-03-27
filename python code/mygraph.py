import sys
input_list =[]
output_list=[]
nodes_list =[]
edges_list =[]

output_of_gates =[]
input_of_gates =[]
input_of_gates =[]
input2_of_gates =[]
#faulty_edge =[sys.argv[1],sys.argv[2],sys.argv[3]]
faulty_edge =['N23','output2','sa0']  ## INPUT FROM THE USER ,

dict_gate_types ={}
PI= ['PI']

#Expected input file format:
#input /output line : the lines names should be seperated only by commas, no space  
#eg: input G1,G2,G3
#gate connection line: <gate_type><space><gate_name><space> ( <space> <output net followed by input nets seperated by commas only(no space)> <space> ) ;
#eg: nand NAND_01 ( G1,G2,G3 );

f =	open ('c17.v','r')
lines = f.read().splitlines()
for i in lines:
	print i
	list1 = i.split()
	print list1						#donot care about the wire, comments,module or endmodule lines
	if(list1[0]=='input'):
		input_list=list1[1].split(',')
		input_list[-1]=input_list[-1].replace(";","")
	elif(list1[0]=='output'):
		output_list=list1[1].split(',')
		output_list[-1]=output_list[-1].replace(";","")
	elif(list1[0]=='and' or list1[0]=='or' or list1[0]=='nand' or list1[0]=='nor' or list1[0]=='not'):
			
		list3=[]
		for i in  range(2 , len(list1)):
						
			if (i==len(list1)-1):
				list1[i]=list1[i].replace(");","")
			elif (i==2):
				list1[i]=list1[i].replace("(","")
				list1[i]=list1[i].replace(",","")
					
			else : 
				list1[i]=list1[i].replace(",","")
			list3.append(list1[i][0:len(list1)])
		
		output_of_gates.append(list3[0])
		input_of_gates.append(list3[1:])
		dict_gate_types[list3[0]]=list1[0]
			
f.close()			

			
		
		

#------------------fanout_list_dictionary_making comparing the inputs of gates------------------------------
#key = name of the node whose output is fanning out
#value = fanout#number  --name for the fanout node
temp_list=[]

print "input_of_gates",input_of_gates
temp_list =[j for i in input_of_gates for j in i]

fanout_dict ={}
fanout_list =[]


for i in temp_list:
	if (temp_list.count(i)>1 and (i not in fanout_list)):
		fanout_list.append(i)
print "fanout_list",fanout_list

for i in range(len(fanout_list)):
	data	= "fanout" + str(i+1)
	fanout_dict[fanout_list[i]]=data
print "fanout_dict",fanout_dict

#---------------Output_dictionary_making-------------------------------------
#key = name of the gate/node whose output are the primary outputs
#value = outout#number --name for the outout node
output_dict	={}
for i in range(len(output_list)):
	data	= "output" + str(i+1)
	output_dict[output_list[i]]=data
print "output_dict",output_dict


print "dict_gate_types",dict_gate_types
nodes_list =	input_list	+	output_of_gates + output_dict.values() +fanout_dict.values() + PI

print "input_of_gates",input_of_gates



#---Insert the fanout node in input1_of_g
#lis[lis.index('one')] = 'replaced!'
for i in input_of_gates:
	for j in i:
		if(j in fanout_dict.keys()):
			print j
			input_of_gates[input_of_gates.index(i)][i.index(j)]=fanout_dict[j]

print "input_of_gates",input_of_gates



#------------------------------------------
for key, value in fanout_dict.iteritems():
	 edges_list.append((key,value))
	 print "(fanout_dict.keys(),fanout_dict.values())",type((key,value))

for key, value in output_dict.iteritems():
	 edges_list.append((key,value))
	 print "output",(key,value)


for i in range(len(output_of_gates)):
	for j in range(len(input_of_gates[i])):
		print "input_of_gates[i][j]",input_of_gates[i][j]
		edges_list.append((input_of_gates[i][j],output_of_gates[i]))


for i in range(len(input_list)):
	edges_list.append(('PI',input_list[i]))


print "edges_list",edges_list		

print "input_list",input_list
print "fanout_dict",fanout_dict
print "output_of_gates",output_of_gates
print "output_list",output_list

#print "wire_list",wire_list

print "**************************************"

print "nodes_list",nodes_list




#**************************************************************************************************************************
#***************************************Constructing the graph*************************************************************
#**************************************************************************************************************************


import networkx as nx 
G = nx.DiGraph()


for i in nodes_list:
	print i
	if(i in input_list):
		G.add_node(i,type='input',cc0=1,cc1=1) 
	elif(i in fanout_dict.values()):
		G.add_node(i,type='fanout',cc0=1,cc1=1)
	elif(i in output_of_gates):
		G.add_node(i,type='gate',gate_type=dict_gate_types[i],cc0=1,cc1=1)
	elif(i in output_dict.values()):
		G.add_node(i,type='output',cc0=1,cc1=1)
	elif(i in 'PI' ):
		G.add_node('PI',type='check',cc0=1,cc1=1)
	
print "G.node:","\n",G.node(data=True) 


for i in range(len(edges_list)):
#	print edges_list[i]
#	print edges_list[i][0]	
#	print edges_list[i][1]
	G.add_edge(edges_list[i][0],edges_list[i][1],value_non_fault='x',value_faulty='x', fault='',CO='x')

G.add_edge(faulty_edge[0],faulty_edge[1], value_non_fault='x',value_faulty='x',fault=faulty_edge[2],CO='x')
	
print "\n G.edges","\n",G.edges	
print "\n end"

#import matplotlib.pyplot as plt
#nx.draw_circular(G)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.savefig("samplegraph.png")


