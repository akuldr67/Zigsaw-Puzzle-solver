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

#take input - its random
pieces=[]
for filename in os.listdir(os.getcwd()+'/puzzle'):
	img = mpimg.imread(os.getcwd()+'/puzzle/'+filename)
	# print(filename)
	pieces.append(img)

#pre-processing
def give_edges(piece):
	l=len(piece)-1
	w=len(piece[0])-1
	ex=[]
	p2=copy.copy(piece)
	p2=np.transpose(p2,(1,0,2))

	ex.append(p2[0])	#left edge
	ex.append(piece[0])	#top edge
	ex.append(p2[w])	#right edge
	ex.append(piece[l])	#bottom edge
	return ex

edges=[]
for piece in pieces:
	edges.extend(give_edges(piece))

p2=copy.copy(pieces)
e2=copy.copy(edges)

done=[]
Rf=[]

def give_piece_no(edge_no):
	xx = math.ceil((edge_no*1.0)/4.0)
	if xx == math.floor((edge_no*1.0/4.0)):
		return (int)(xx+1)
	else:
		return (int)(xx)

def give_edge_nos(piece_no):
	xx = (piece_no-1)*4
	return [xx,xx+1,xx+2,xx+3]


#Initialize
Rr=list(xrange(len(edges)))
done.append(1)
Rf.extend(give_edge_nos(1))

for qq in Rf:
	Rr.remove(qq)


def match_edges(e1,e2):
	loss=0
	ll = len(edges[e1])
	ed1 = copy.copy(edges[e1])
	ed2 = copy.copy(edges[e2])
	ed1 = np.asarray(ed1)
	ed2 = np.asarray(ed2)
	for ind in range(0,ll):
		loss += np.linalg.norm(ed1[ind]-ed2[ind])
	return loss


threshold = 10
# If got error Rf is empty (list index out of range)...increse the threshold. 
# Generally works great for threshold equals around 10 for a 5x5 puzzle. 

to_show = []
c1 = (0,0)
c2 = (0,len(p2[0][0])-1)
c3 = (len(p2[0])-1,0)
c4 = (len(p2[0])-1,len(p2[0][0])-1)
to_show.append([1,c1,c2,c3,c4])


max_x = max([qw[4][0] for qw in to_show])
max_y = max([qw[4][1] for qw in to_show])
ss1 = (max_x+1,max_y+1,4)
output = np.ones(ss1)

for ii in range(0,len(p2[0])):
	for jj in range(0,len(p2[0][0])):
		output[ii][jj] = p2[0][ii][jj]


imgp = plt.imshow(output)
# plt.show()
plt.show(block=False)
plt.pause(0.2)
plt.close()


while(len(Rr)!=0):
	x = Rf[0]
	# x = random.choice(Rf)
	x_len = len(edges[x])
	valid = []
	for ed in Rr:
		if(len(edges[ed]) == x_len):
			valid.append(ed)


	original_piece = give_piece_no(x)
	new_valid = []
	if((original_piece-1)*4 == x):	#if old is left edge
		for vv in valid:
			if(((give_piece_no(vv)-1)*4)+2 == vv): #if vv is a right edge
				new_valid.append(vv)

	if(((original_piece-1)*4)+1 == x): #if old is top edge
		for vv in valid:
			if(((give_piece_no(vv)-1)*4)+3 == vv): #if vv is a bottom edge
				new_valid.append(vv)

	if(((original_piece-1)*4)+2 == x): #if old is right edge
		for vv in valid:
			if(((give_piece_no(vv)-1)*4) == vv): #if vv is a left edge
				new_valid.append(vv)

	if(((original_piece-1)*4)+3 == x): #if old is bottom edge
		for vv in valid:
			if(((give_piece_no(vv)-1)*4)+1 == vv): #if vv is a top edge
				new_valid.append(vv)
	valid = copy.copy(new_valid)

	#now match
	loss=[]
	for ed in valid:
		ld = match_edges(x,ed)
		loss.append(ld)

	min_loss = min(loss)
	min_ind = valid[loss.index(min(loss))]

	if(min_loss>threshold):
		Rf.remove(x)

	else:
		piece_no_added = give_piece_no(min_ind)
		# print(piece_no_added,min_ind,x)
		done.append(piece_no_added)
		Rf.remove(x)
		to_remove = give_edge_nos(piece_no_added)

		for eds in to_remove:
			if (eds in Rr):
				Rr.remove(eds)
		Rf.extend(to_remove)
		if (min_ind in Rf):
			Rf.remove(min_ind)



		c11 = (0,0)
		c22 = (0,0)
		c33 = (0,0)
		c44 = (0,0)
		n_l = len(p2[piece_no_added-1])
		n_w = len(p2[piece_no_added-1][0])

		qx = [ass[0] for ass in to_show]
		x_index = qx.index(give_piece_no(x))
		ori_corners = copy.copy(to_show[x_index])
		q1 = ori_corners[1]
		q2 = ori_corners[2]
		q3 = ori_corners[3]
		q4 = ori_corners[4]
		

		if((original_piece-1)*4 == x):	#if old is left edge
			c22 = (q1[0],q1[1]-1)
			c44 = (q3[0],q3[1]-1)
			c11 = (c22[0],c22[1]-n_w+1)
			c33 = (c44[0],c44[1]-n_w+1)

		if(((original_piece-1)*4)+1 == x): #if old is top edge
			c33 = (q1[0]-1,q1[1])
			c44 = (q2[0]-1,q2[1])
			c11 = (c33[0]-n_l+1,c33[1])
			c22 = (c44[0]-n_l+1,c44[1])

		if(((original_piece-1)*4)+2 == x): #if old is right edge
			c11 = (q2[0],q2[1]+1)
			c33 = (q4[0],q4[1]+1)
			c22 = (c11[0],c11[1]+n_w-1)
			c44 = (c33[0],c33[1]+n_w-1)

		if(((original_piece-1)*4)+3 == x): #if old is bottom edge
			c11 = (q3[0]+1,q3[1])
			c22 = (q4[0]+1,q4[1])
			c33 = (c11[0]+n_l-1,c11[1])
			c44 = (c22[0]+n_l-1,c22[1])


		to_show.append([piece_no_added,c11,c22,c33,c44])

		#for show :shift:
		min_x = min([qw[1][0] for qw in to_show])
		max_x = max([qw[4][0] for qw in to_show])
		min_y = min([qw[1][1] for qw in to_show])
		max_y = max([qw[4][1] for qw in to_show])
		
		dx = 0
		dy = 0
		if(min_x<0):
			dx = 0-min_x
		if(min_y<0):
			dy = 0-min_y

		for ff in range(0,len(to_show)):
			for ee in range(1,5):
				to_show[ff][ee] = (to_show[ff][ee][0]+dx,to_show[ff][ee][1]+dy)
	

		# to_show.sort()
	

		cc = 1
		max_x = max([qw[4][0] for qw in to_show])
		max_y = max([qw[4][1] for qw in to_show])
		ss1 = (max_x+1,max_y+1,4)
		output = np.ones(ss1)
		for entry in to_show:
			# print (entry[0]-1,cc)
			xi = 0
			for ii in range(entry[1][0],entry[3][0]):
				yi = 0
				for jj in range(entry[1][1],entry[2][1]):
					output[ii][jj] = p2[entry[0]-1][xi][yi]
					yi+=1
				xi+=1
			cc+=1


		imgp = plt.imshow(output)
		# plt.show()
		plt.show(block=False)
		plt.pause(0.2)
		plt.close()



		#checking...:
		pt1 = [pts[1] for pts in to_show]	#1st
		pt2 = [pts[2] for pts in to_show]	#2nd
		pt3 = [pts[3] for pts in to_show]	#3rd
		pt4 = [pts[4] for pts in to_show]	#4th

		pt_above = (c11[0]-1+dx,c11[1]+dy)
		pt_right = (c22[0]+dx,c22[1]+1+dy)
		pt_below = (c33[0]+1+dx,c33[1]+dy)
		pt_left = (c11[0]+dx,c11[1]-1+dy)

		#checking above - pt_above present in :
		left_edge = to_remove[0]
		above_edge = to_remove[1]
		right_edge = to_remove[2]
		below_edge = to_remove[3]

		if(pt_left in pt2):
			if(left_edge in Rr):
				Rr.remove(left_edge)
			if(left_edge in Rf):
				Rf.remove(left_edge)
			#remove right edge of left piece
			already_piece = to_show[pt2.index(pt_left)][0]
			new_r_edge = give_edge_nos(already_piece)[2]
			if(new_r_edge in Rr):
				Rr.remove(new_r_edge)
			if(new_r_edge in Rf):
				Rf.remove(new_r_edge)


		if(pt_above in pt3):
			if(above_edge in Rr):
				Rr.remove(above_edge)
			if(above_edge in Rf):
				Rf.remove(above_edge)
			#remove bottom edge of piece above
			already_piece = to_show[pt3.index(pt_above)][0]
			new_b_edge = give_edge_nos(already_piece)[3]
			if(new_b_edge in Rr):
				Rr.remove(new_b_edge)
			if(new_b_edge in Rf):
				Rf.remove(new_b_edge)


		if(pt_right in pt1):
			if(right_edge in Rr):
				Rr.remove(right_edge)
			if(right_edge in Rf):
				Rf.remove(right_edge)
			#remove left edge of right piece
			already_piece = to_show[pt1.index(pt_right)][0]
			new_l_edge = give_edge_nos(already_piece)[0]
			if(new_l_edge in Rr):
				Rr.remove(new_l_edge)
			if(new_l_edge in Rf):
				Rf.remove(new_l_edge)


		if(pt_below in pt1):
			if(below_edge in Rr):
				Rr.remove(below_edge)
			if(below_edge in Rf):
				Rf.remove(below_edge)
			#remove top edge of bottom piece
			already_piece = to_show[pt1.index(pt_below)][0]
			new_t_edge = give_edge_nos(already_piece)[1]
			if(new_t_edge in Rr):
				Rr.remove(new_t_edge)
			if(new_t_edge in Rf):
				Rf.remove(new_t_edge)


print("done!")
imgp = plt.imshow(output)
# plt.savefig("output.jpg")
plt.show()