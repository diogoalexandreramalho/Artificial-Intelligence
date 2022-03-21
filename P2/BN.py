# Diogo Ramalho - 86407 & Manuel Manso - 86471  Grupo 42
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

from itertools import product


class Node():
	def __init__(self, prob, parents = []):
		self.probabilities = prob
		self.parents = parents
	
	def computeProb(self, evid):
		indexes = ()
		if len(self.parents) == 0:
			indexes = (0)
		for a in self.parents:
			indexes += (evid[a],)

		prob = self.probabilities[indexes]
		return [1-prob, prob]

	
class BN():
	def __init__(self, gra, prob):
		self.graph = gra
		self.probabilities = prob

	def computePostProb(self, evid):

		ap = []
		bp = []
		j=0

		for i in evid:
			if i==[]:
				j+=1
		
		a = [ list(evid) for _ in range(2**j)]
		b = [ list(evid) for _ in range(2**j)]

		comb = list(product([0,1],repeat = j))

		for i in range(len(comb)):
			count=0
			for j in range(len(a[i])):
				if a[i][j]==-1:
					a[i][j]=1
					b[i][j]=0

				elif a[i][j]==[]:
					a[i][j]=comb[i][count]
					b[i][j]=comb[i][count]
					count+=1


		for i in range(len(a)):
			a[i] = tuple(a[i])
			b[i] = tuple(b[i])
			ap.append(self.computeJointProb(a[i]))
			bp.append(self.computeJointProb(b[i]))

		
		c= sum(ap)/(sum(ap)+sum(bp))
		
		return c
		
		
	def computeJointProb(self, evid):
		prob = 1
		i = 0
		for node in self.probabilities:
			prob *= node.computeProb(evid)[evid[i]]
			i+=1 

		return prob

