# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:18:18 2018

@author: Rahman Khorramfar
"""
import numpy as np;
rnd = np.random; rnd.seed(25);

M = 50 # first stage items
N = 20; # Number of knapsacks
K = 50; # Number of items in the second stage
Omega = 10; # Number of scenarios


a = rnd.uniform(1,100,M);  # weight associated with item i in M
c = rnd.uniform(10,50,M); # profit associated with item i in M
W = rnd.uniform(10,100,K);  # weight associated with item k in K
p = rnd.rand(Omega); p = p/p.sum(); # probability of each scenario
q = rnd.uniform(10,50,(K,Omega));  # profit of item k under scenario w
b = rnd.uniform(100,200,N);  # capacity of each knapsack

c = np.round(c); W = np.round(W);  q = np.round(q);
a = np.round(a); b = np.round(b);

