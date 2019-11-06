# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 14:48:26 2018

@author: Rahman Khorramfar
L-Shape Method for stochastic knapsack problem
"""
import numpy as np; 
import SP;
from ProblemData import M,N,K,Omega,a,c,W,b,p,q;
import time

#%% Get the initial solution (x)
xs,initobj = SP.InitialSol(); EQ = []; # 
Thetas = []; # theta is set to a large number for this problem at the beginning
Thetas.append(10e+4);

#%%  get H and T matrices. create some sets. Get upper bound (U) for the Integer Lshape
ht = SP.Get_h_T();
H = ht[0]; T = ht[1]; 
cuts = []; icuts=[];
MP_obj =[]; IntEQ = []; U = 0 ; 
MP_obj.append(initobj);

for w in range(Omega): 
    U += p[w]*SP.Integer_Recourse_obj(np.zeros((M,N)),w);
	
#%% Main Loop
current_time = time.time()
while True:	#abs(Thetas - EQ)>10e-2
    rts = []; ieq = 0;
    for w in range(Omega):
        # rt[0]= objective function, rt[1] dual of cons 3, rt[2] dual of cons 4
        rt = SP.SolveSP(xs,w);
        rts.append(rt); 		rt=[]; 
        ieq += p[w]*SP.Integer_Recourse_obj(xs,w);
        #EQ += p[w]*rt[0];
        
    EQ.append(SP.Recourse_Expected_Value(xs,H,T,rts));
    IntEQ.append(ieq);
    #if  abs(EQ[len(EQ)-1]- Thetas[len(Thetas)-1]) <= 1: # EQ[len(EQ)-1] >= Thetas ==> it is optimal
    #	print('\n\n Objective Function: ', MP_obj[len(MP_obj)-1]);
		
    if EQ[len(EQ)-1] < Thetas[len(Thetas)-1]: # if not optimal for LP add optimality cut
        cuts.append(rts);
	
    if IntEQ[len(IntEQ)-1] >= Thetas[len(Thetas)-1] or (time.time() - current_time) >= 1000:
        print('\n\n Objective Function: ', MP_obj[len(MP_obj)-1]);
        print('\n Elapsed time is: ', time.time() - current_time)
        break;
    else: # add optimality cut of the integer Lshape
        icuts.append(SP.Integer_Cut(xs,ieq,U));
		
    # add the optimality cut solve the MP and get values of x and theta
    rt = SP.SolveMP(cuts,H,T, icuts);	
    MP_obj.append(rt[0]);
    xs = rt[2]; # update x
    Thetas.append(rt[1]); # update Theta
    #print(Thetas, '\t', EQ);
    #print('*****************');

	
	
	




