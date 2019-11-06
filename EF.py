# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 23:38:46 2018

@author: Rahman Khorramfar
https://www.ibm.com/support/knowledgecenter/en/SSSA5P_12.6.3/ilog.odms.cplex.help/refpythoncplex/html/cplex._internal._subinterfaces.LinearConstraintInterface-class.html#add

https://www.ibm.com/support/knowledgecenter/en/SSSA5P_12.6.1/ilog.odms.cplex.help/refpythoncplex/html/cplex._internal._subinterfaces.SolutionInterface-class.html#get_dual_values

use link above to get help about cplex python API
"""

#from KnapsackData import M,N,K,Omega,a,c,w,b,p,q;
#%% Generate Data
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:19:45 2018

@author: Rahman Khorramfar
"""
import numpy as np;
rnd = np.random; rnd.seed(25);
from ProblemData import M,N,K,Omega,a,c,W,b,p,q;

#%%

import cplex;
# Create the modeler/solver.
cpx = cplex.Cplex();
cpx.objective.set_sense(cpx.objective.sense.maximize);
#%% Create variables
x = [None]*M;  # item i in M assigned to knapsack j in N
for i in range(M):
  	x[i] = list(cpx.variables.add(obj = [c[i]]*N,
								   lb=[0]*N,
								   ub=[1]*N,
								   types=['B']*N,
								   names=['x(%d)(%d)'%(i,j) for j in range(N)]));

#y = np.empty((K,N,Omega));
y = np.zeros((K,N,Omega));
y = y.tolist();
for k in range(K):
	for n in range(N):
		y[k][n]= list(cpx.variables.add(obj = p*q[k],
								   lb=[0]*Omega,
								   ub=[1]*Omega,
								   types=['B']*Omega,
								   names=['y(%d)(%d)(%d)'%(k,n,w) for w in range(Omega)]));

#%% Constraints
# Constraint 1		
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
			
# Constraint 3
for j in range(N):
	for w in range(Omega):
		ind = [x[i][j] for i in range(M)] + [y[k][j][w] for k in range(K)];	
		
		val = [a[i] for i in range(M)] + [W[k] for k in range(K)];	
		
		cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
            senses=['L'],rhs=[b[j]], names = ['C03']);     
			
# Constraint 4

for k in range(K):
	for w in range(Omega):
		ind = [y[k][j][w] for j in range(N)];
		val = [1.0]*N;				
		name = 'C04'+str(k)+str(w);
		cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
            senses=['L'],rhs=[1.0], names = [name]);
							

cpx.parameters.preprocessing.linear.set(0);
#cpx.parameters.tuning_status.time_limit(10);

#cpx.parameters.tuning.timelimit.set(3)
#cpx.parameters.mip.dettimelimit(2);
# Turn off CPLEX logging
#cpx.parameters.mip.display.set(0);				
cpx.solve();
cpx.write('EF.lp');
print("Solution status =", cpx.solution.get_status_string());
print("Optimal value:", cpx.solution.get_objective_value());
xs = np.zeros((M,N));
for i in range(M):
	xs[i] = cpx.solution.get_values(x[i]);
#print(xs)
ys =np.zeros((K,N,Omega));
for k in range(K):
	for j in range(N):
		ys[k][j] = cpx.solution.get_values(y[k][j]);
#print(ys);
# Get dual variabls for the constraint 4
#c4d = np.zeros((K,Omega));
#c4d = c4d.tolist();
#for k in range(K):
#	for w in range(Omega):
#		name = 'C04'+str(k)+str(w);
#		c4d[k][w] = cpx.solution.get_dual_values([name]);
#print(c4d)
				
				
				