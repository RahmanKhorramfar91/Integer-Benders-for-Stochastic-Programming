# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:19:45 2018

@author: Rahman Khorramfar
"""











def Integer_Recourse_obj(xs,w):
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	import cplex;

# Create the modeler/solver.
	cpx = cplex.Cplex();
	cpx.objective.set_sense(cpx.objective.sense.maximize);
	y = np.zeros((K,N));
	y = y.tolist();	
	
	for k in range(K):
		#print([q[k][w]]*N);
		y[k]= list(cpx.variables.add(obj = [q[k][w]]*N,
								   lb=[0]*N,
								   ub=[1.0]*N,types=['B']*N,
								   names=['y(%d)(%d)(%d)'%(w,k,n) for n in range(N)]));
								   #types=['B']*N,names=['y(%d)(%d)'%(k,n) for n in range(N)]
								   
# Constraint 3
	for j in range(N):
		b0 = 0;
		for i in range(M):
			b0+= a[i]*xs[i][j];
		ind =  [y[k][j] for k in range(K)];				
		val =  [W[k] for k in range(K)];			
		cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
			  senses=['L'],rhs=[b[j]-b0]);     
				
# Constraint 4
	for k in range(K):
		ind = [y[k][j] for j in range(N)];
		val = [1.0]*N;				
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[1.0]);
	
	cpx.solve();	
	
	return cpx.solution.get_objective_value();





def Recourse_Expected_Value(xs,H,T,rts):
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	
	rhs1 = 0; val1 = np.zeros(M*N);
	for w in range(Omega):
		rhs1 += p[w]* (sum(rts[w][1]*H));
		for i in range(M*N):
			val1[i] += p[w]*sum(rts[w][1]*T[:,i]);
	xss = [xs[i][j] for i in range(M) for j in range(N)];
	Wv = rhs1-sum(val1*xss);
	
	return Wv;
	
	
	
	
def Get_h_T():
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	H = np.ones(K+N);
	for i in range(N):
		H[i] = b[i];
		
	T = np.zeros((N+K,M*N));
		
	shift = 0;
	for j in range(N):
		for i in range(M):
			T[j][shift+i*N] = a[i];
		shift += 1;
	
	return H,T;



def InitialSol():
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	
	# Create the modeler/solver.	
	import cplex;
	cpx = cplex.Cplex();
	cpx.objective.set_sense(cpx.objective.sense.maximize);
	
	#Create variable of the Master problem
	x = np.zeros((M,N));
	x = x.tolist();  # item i in M assigned to knapsack j in K
	for i in range(M):
	  	x[i] = list(cpx.variables.add(obj = [c[i]]*N,
				  lb=[0]*N,ub=[1]*N,types=['B']*N,
				  names=['x(%d)(%d)'%(i,j) for j in range(N)]));

	# Master problem
	# Constraint 1		
	for j in range(N):
		ind = [x[i][j] for i in range(M)];
		val = [a[i] for i in range(M)];
		
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[b[j]]);
				
	# Constraint 2
	for i in range(M):
		ind = [x[i][j] for j in range(N)];	
		val = [1.0]*N;
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[1.0]);						 
							 
	cpx.solve();
#	cpx.write('InitialSol.lp');
#	print("Solution status for the initial Solution =", cpx.solution.get_status_string());
#	print("Optimal value of the initial solution:", cpx.solution.get_objective_value());

	
	# Get the values of x 
	xs = np.zeros(np.shape(x));
	for i in range(M):
		xs[i] = cpx.solution.get_values(x[i]);
	
		
	return xs,cpx.solution.get_objective_value();












def SolveSP(xs,w):
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	import cplex;

# Create the modeler/solver.
	cpx = cplex.Cplex();
	cpx.objective.set_sense(cpx.objective.sense.maximize);
	y = np.zeros((K,N));
	y = y.tolist();	
	
	for k in range(K):
		#print([q[k][w]]*N);
		y[k]= list(cpx.variables.add(obj = [q[k][w]]*N,
								   lb=[0]*N,
								   ub=[cplex.infinity]*N,names=['y(%d)(%d)(%d)'%(w,k,n) for n in range(N)]));
								   #types=['B']*N,names=['y(%d)(%d)'%(k,n) for n in range(N)]
								   
# Constraint 3
	for j in range(N):
		b0 = 0;
		for i in range(M):
			b0+= a[i]*xs[i][j];
		ind =  [y[k][j] for k in range(K)];				
		val =  [W[k] for k in range(K)];	
		name01 = 'C03'+str(j);
		cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
			  senses=['L'],rhs=[b[j]-b0], names = [name01]);     
				
# Constraint 4
	name0 = [];
	for k in range(K):
		ind = [y[k][j] for j in range(N)];
		val = [1.0]*N;				
		name0.append('C04'+str(k));
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[1.0], names = [name0[len(name0)-1]]);
	
	cpx.solve();	
	#name = 'SP'+str(w+1)+'.lp';
	#cpx.write(nam);

	
	c5d = np.zeros(N+K);
	c5d = cpx.solution.get_dual_values();
	
	rt = (cpx.solution.get_objective_value(),c5d);
	return rt;
	
	

















def SolveMP(cuts,H,T, icuts=[]):
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	
	# Create the modeler/solver.
	
	import cplex;
	cpx = cplex.Cplex();
	cpx.objective.set_sense(cpx.objective.sense.maximize);
	
	#Create variable of the Master problem
	x = np.zeros((M,N));
	x = x.tolist();  # item i in M assigned to knapsack j in K
	for i in range(M):
	  	x[i] = list(cpx.variables.add(obj = [c[i]]*N,
				  lb=[0]*N,ub=[1]*N,types=['B']*N,
			     names=['x(%d)(%d)'%(i,j) for j in range(N)]));
									   	
	theta= cpx.variables.add(obj=[1.0],lb=[0.0],ub=[cplex.infinity],
							      names = ['Theta']);
							 
	
	# Master problem
	# Constraint 1		
	C1Dual = np.zeros(N);
	C1Dual = C1Dual.tolist();
	for j in range(N):
		ind = [x[i][j] for i in range(M)];
		val = [a[i] for i in range(M)];
		
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[b[j]], names = ['C01']);
				
	# Constraint 2
	for i in range(M):
		ind = [x[i][j] for j in np.arange(N)];	
		val = [1.0]*N;
		cpx.linear_constraints.add(
	            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
	            senses=['L'],rhs=[1.0], names = ['C02']);						 

	# add cuts from continuous Lshape
	for s in cuts:
		ind = [theta[0]] + [x[i][j] for i in range(M) for j in range(N)];
		
		rhs1 = 0; val1 = np.zeros(M*N);
		for w in range(Omega):
			rhs1 += p[w]* (sum(s[w][1]*H));
			for i in range(M*N):
				val1[i] += p[w]*sum(s[w][1]*T[:,i]);
		val = [1.0] + val1.tolist();
		cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=ind, val=val)],
									   senses=['L'],rhs=[rhs1]);

	# Add cuts from integer Lshape
	for s in icuts:
		ind = [theta[0]] + [x[i][j] for i in range(M) for j in range(N)];
		cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=ind, val=s[0])],
									   senses=['L'],rhs=[s[1]]);		

									   
	# Get the values of x  and theta
	cpx.solve();
	cpx.write('MP.lp');
	
	xi = np.zeros(np.shape(x));
	for i in range(M):
		xi[i] = cpx.solution.get_values(x[i]);
	
	Thetas = cpx.solution.get_values(theta[0]);
	rt = [cpx.solution.get_objective_value(), Thetas, xi];
	return rt;
	


def Integer_Cut(xs,Qx,U):
	import numpy as np;
	from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
	
	S = sum(sum(xs));
	rhs = Qx+(U-Qx)*S;
	
	val = np.zeros(M*N); val= val.tolist();
	#ind[0] = 1;
	for i in range(M):
		for j in range(N):
			if np.round(xs[i][j]) ==1:
				val[i*N+j] = U-Qx;
			else:
				val[i*N+j] = Qx-U;
				
	val = [1]+val;
	return val,rhs;


#
#import cplex;
#cpx = cplex.Cplex();
#cpx.objective.set_sense(cpx.objective.sense.maximize);
#
##%% Create variable of the Master problem
#x = np.zeros((M,K));
#x = x.tolist();  # item i in M assigned to knapsack j in K
#for i in range(M):
#  	x[i] = list(cpx.variables.add(obj = [c[i]]*K,
#			  lb=[0]*K,
#								   ub=[1]*K,
#								   types=['B']*K,
#								   names=['x(%d)(%d)'%(i,j) for j in range(K)]));
#
#theta= cpx.variables.add(obj=[0.0],lb=[0.0],ub=[cplex.infinity],
#						      names = ['Theta']);
#						 
#
##%% Master problem
## Constraint 1		
#C1Dual = np.zeros(N);
#C1Dual = C1Dual.tolist();
#for j in range(N):
#	ind = [x[i][j] for i in range(M)];
#	val = [a[i] for i in range(M)];
#	
#	cpx.linear_constraints.add(
#            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
#            senses=['L'],rhs=[b[j]], names = ['C01']);
#			
## Constraint 2
#for i in range(M):
#	ind = [x[i][j] for j in np.arange(N)];	
#	val = [1.0]*N;
#	cpx.linear_constraints.add(
#            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
#            senses=['L'],rhs=[1.0], names = ['C02']);						 
#						 
#cpx.solve();
#print("Solution status =", cpx.solution.get_status_string());
#print("Optimal value:", cpx.solution.get_objective_value());
#
#
##%% Get the values of x 
#xs = np.zeros(np.shape(x));
#for i in range(M):
#	xs[i] = cpx.solution.get_values(x[i]);
