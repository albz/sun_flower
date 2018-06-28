# Date:			02-02-2012
# Purpose:      reading csv matrixes
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string
import time,datetime
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
import matplotlib
### --- ###

#time format
time_format = "%Y/%m/%d %H:%M:%S"


###---### read DATETIME first 2 colums
def read_csv_datetime(path,fname):
	#util
	SP_time_str      = [];
	SP_date_str      = [];
	SP_datetime      = [];

	#reading file
	read = csv.reader(open(os.path.join(path,fname), "r"),delimiter=';',quoting=csv.QUOTE_NONE)
 
	#split and organize
	for row in read:
		SP_date_str.append(str(row[0]))
		SP_time_str.append(str(row[1]))
	
	del SP_time_str[0:2] #removign heardes
	del SP_date_str[0:2] #removign heardes

	#date+time str->num datetime
	l = len(SP_date_str)
	for count in range(0,l):
	  	timestring = "%s %s" % (SP_date_str[count],SP_time_str[count])
	  	SP_datetime.append(datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format))))
	  	
	return SP_datetime
   	



###---### read ANY OTHER csv column
def read_csv_generic_column(path,fname,ncolumn):

	#util
	SP_pow_str       = [];
	SP_pow           = [];

	#reading file
	read = csv.reader(open(os.path.join(path,fname), "r"),delimiter=';',quoting=csv.QUOTE_NONE)
 
	#split and organize
	for row in read:
		tmp = str(row[ncolumn]); tmp = tmp.replace(',','.')
		if tmp == '':
			tmp = 'NaN'
		SP_pow_str.append(tmp)
	
	del SP_pow_str[0:2]  #removign headers

	#Irradiance str->num
	for line in SP_pow_str:
		try:
			SP_pow.append(float(line))
		except ValueError:
			pass

	return SP_pow