# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 14:48:26 2018

@author: Rahman Khorramfar
L-Shape Method for stochastic knapsack problem
"""
import numpy as np; 
import SP;
from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
import time;
current = time.time();

#%% Get the initial solution (x)
xs,initialOBj = SP.InitialSol(); EQ = []; # 
Thetas = 10e+8; # theta is set to a large number for this problem at the beginning

# get H and T matrices
ht = SP.Get_h_T();
H = ht[0]; T = ht[1]; 
cuts = []; MP_obj =[]; MP_obj.append(initialOBj);
#%% Main Loop
while True:	#abs(Thetas - EQ)>10e-2
	
	rts = [];
	for w in range(Omega):
	# rt[0]= objective function, rt[1] dual of cons 3, rt[2] dual of cons 4
		rt = SP.SolveSP(xs,w);
		rts.append(rt); 		rt=[];  
		#EQ += p[w]*rt[0];
 
	EQ.append(SP.Recourse_Expected_Value(xs,H,T,rts));
	
	if  abs(EQ[len(EQ)-1]- Thetas) <= 1:
		print('\n\n Objective Function: ', MP_obj[len(MP_obj)-1]);
		break
	cuts.append(rts);
	
	# add the optimality cut solve the MP and get values of x and theta
	rt = SP.SolveMP(cuts,H,T);	
	MP_obj.append(rt[0]);
	xs = rt[2];
	Thetas = rt[1];
	#print(Thetas, '\t', EQ);
	#print('*****************');

	
	
	
#%% Plot the results
print('Elapsed Time: ', time.time()-current);	



