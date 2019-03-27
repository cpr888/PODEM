
def AND_gate(input_list):
	flag =0
	
	for input in input_list:
			
			if(input=='0'):			#Controlling_value = 0, if present , output = 0
				return '0'					
			else:
				if(input=='X'):
					flag =1			#If there is atleast 1 value= X
					
	if(flag==1):					
		return 'X'					#If there is atleast 1 value = X and no control value, output =X	
	else:
		return '1' 					#All input is '1'
		
		
def OR_gate(input_list):
	flag =0
	
	for input in input_list:
			if(input=='1'):	
				return '1'			#Controlling_value = 1, if present , output = 1
			else:
				if(input=='x'):
					flag =1			#keep track if there is atleast 1 value= X
					
	if(flag==1):
		return 'x'					#If there is atleast 1 value = X and no control value, output =X	
	else:
		return '0' 					#All input is '0'


def NAND_gate(input_list):
	flag =0
	
	for input in input_list:
			if(input=='0'):	
				return '1'			#Controlling_value = 0, if present , output = 1
			else:
				if(input=='x'):
					flag =1			#keep track if there is atleast 1 value= X
					
	if(flag==1):
		return 'x'					#If there is atleast 1 INPUT value = X and no control value, output =X	
	else:
		return '0' 					#All input is '1'
		
		
def NOR_gate(input_list):
	flag =0
	
	for input in input_list:
			if(input=='1'):
				return '0'			#Controlling_value = 1, if present , output = 0
			else:
				if(input=='x'):
					flag =1			#keep track if there is atleast 1 value = X
					
	if(flag==1):
		return 'x'					#If there is atleast 1 INPUT value = X and no control value, output =X	
	else:
		return '1' 					#All input is '0'
		
		

def XOR_gate(input_list):
	flag =0
	count =0
	for input in input_list:
			if(input=='x'):
				return 'x'
			else:
				if(input=='1'):
					count =count +1
					
	if(count % 2 !=0):				#Odd no of 1
		return '1'
	else:
		return '0' 
		

def XNOR_gate(input_list):
	flag =0
	count =0
	for input in input_list:
			if(input=='x'):
				return 'x'
			else:
				if(input=='1'):
					count =count +1
					
	if(count % 2 ==0):				#Even no of 1
		return '1'
	else:
		return '0' 



			
def NOT_gate(a):
	return {
			'0':'1',
			'1':'0',
			'x':'x'
			}[a]	

def BUFFER_gate(a):
	return {
			'0':'0',
			'1':'1',
			'x':'x'
			}[a]	
