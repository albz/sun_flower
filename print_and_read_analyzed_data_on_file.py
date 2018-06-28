#!/usr/bin/python
######################################################################
# Name:         print_and_read_analyzed_data_on_file
# Author:       A. Marocchino
# Date:			14-08-2012
# Purpose:      print and read already analyzed data to speed up the process
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string, ftplib
import time, datetime, math
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
###>>>


#print data on a file
def print_analyzed_data_on_file(mode,name_output_file,vector,folder):

	file = os.path.join(os.path.join(os.getcwd(),folder),name_output_file)
	f    = open(file,'w')
	
	if mode == 'date':
		for i in range(0,len(vector)):
			f.writelines(vector[i].strftime('%Y_%m_%d')+'\n')
	if mode == 'datetime':
		for i in range(0,len(vector)):
			f.writelines(vector[i].strftime('%Y_%m_%d_%H_%M_%S')+'\n')
	if mode == 'value':
		for i in range(0,len(vector)):
			f.writelines('%e \n' % vector[i])
	
	f.close()




#read data from a 'saved' file
def read_analyzed_data_on_file(mode,name_output_file,folder):

	vector = []

	file = os.path.join(os.path.join(os.getcwd(),folder),name_output_file)
	
	if os.path.exists(file) == False:
		return vector
	
	f    = open(file,'r')
	if mode == 'date':
		for line in f:
			line = line.split()[0]
			vector.append(datetime.date.fromtimestamp(time.mktime(time.strptime(line, '%Y_%m_%d'))))
	if mode == 'datetime':
		for line in f:
			line = line.split()[0]
			vector.append(datetime.datetime.fromtimestamp(time.mktime(time.strptime(line, '%Y_%m_%d_%H_%M_%S'))))
	if mode == 'value':
		for line in f:
			try:
				vector.append(float(line))
			except ValueError:
				pass
 	f.close()
 	return vector
