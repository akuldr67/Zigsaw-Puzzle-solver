import os
import cv2
import numpy as np
import pickle
import matplotlib
import matplotlib.image as mpimg
from PIL import Image
import matplotlib.pyplot as plt
import random
import copy
import math


FILENAME = 't8.jpg'

nx = 5
ny = 5

#generate the puzzle

tt = Image.open(FILENAME)
sizee = tt.size
finalSize = min(sizee)

def gcd(a,b):
	if(a==0):
		return b
	return gcd(b%a,a)

def lcm(a,b):
	return (a*b)/gcd(a,b)

opt = lcm(nx,ny)

while(finalSize%opt!=0):
	finalSize-=1

tt = tt.resize((finalSize,finalSize),Image.ANTIALIAS)
tt.save(FILENAME)

img = mpimg.imread(FILENAME)
img = np.asarray(img)
l = len(img)
w = len(img[0])
print l,w
x = math.floor(l/nx)
y = math.floor(w/ny)
print x,y

temp = []
i = 0
ni = 1
t=[]
while(i<l):
	temp=[]
	while(i<l and i<(ni*x)):
		temp.append(img[i])
		i+=1
	t.append(temp)
	ni+=1

count = 0 
for rx in t:
	rx1=copy.copy(rx)
	rx1 = np.asarray(rx1)
	rx1 = np.transpose(rx1,(1,0,2))
	j=0 
	nj=1
	while(j<w):
		temp=[]
		while(j<w and j<(nj*y)):
			temp.append(rx1[j])
			j+=1
		temp = np.asarray(temp)
		temp = np.transpose(temp,(1,0,2))
		count+=1
		mpimg.imsave("./puzzle/"+str(count)+'.png',temp)
		nj+=1
