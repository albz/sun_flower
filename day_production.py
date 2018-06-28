# Date:			02-02-2012
# Purpose:      reading solarimetro data
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
import matplotlib.pyplot as plt
### --- ###

#path
path = os.getcwd()

#time format
time_format = "%Y-%m-%d %H:%M:%S"

#one day
one_day = datetime.timedelta(days=1)



###--- SELECTED DAY ---###
def selected_day(dates,quantity,chosen_date):

	#util
	SP_datetime_day_chosen = []
	SP_quanity_day_chosen  = []


	l = len(dates)
	for i in range(0,l):
		if dates[i] > chosen_date and dates[i] < chosen_date + one_day:
			SP_datetime_day_chosen.append(dates[i])
			SP_quanity_day_chosen.append(quantity[i])

	return SP_datetime_day_chosen,SP_quanity_day_chosen



###--- SUM TWO TEMPORAL=DATETIME VECTORS for a given delta ---###
def sum_datetime_vectors(date_1,vector_1,date_2,vector_2,delta):
	#classic slower version
# 	util_1 = []
# 	util_2 = []
# 	for i in range(0,len(date_1)):
# 		for j in range(0,len(date_2)):
# 			if date_1[i]<date_2[j]+delta and date_1[i]>date_2[j]-delta:
# 				i = i
# 				util_1.append( date_1[i] )
# 				util_2.append( vector_1[i]+vector_2[j] )

	#faster function version
	util_1 = []
	util_2 = []
	if len(date_1) < len(date_2):
		for i in range(0,len(date_1)):
			F = numpy.where( abs(array(date_2)-array(date_1[i]) ) < delta)
			S = F[0]
			if len(S) > 0:
				util_1.append( date_1[i] )
				util_2.append( vector_1[i]+vector_2[S[0]] )
	else:
		for i in range(0,len(date_2)):
			F = numpy.where( abs(array(date_1)-array(date_2[i]) ) < delta)
			S = F[0]
			if len(S) > 0:
				util_1.append( date_2[i] )
				util_2.append( vector_1[S[0]]+vector_2[i] )
				
	return util_1,util_2


###--- SUM TWO TEMPORAL=onlyDATE VECTORS ---###
def sum_date_vectors(date_1,vector_1,date_2,vector_2):

	util_1 = []
	util_2 = []
	if len(date_1) < len(date_2):
		for i in range(0,len(date_1)):
			F = numpy.where( abs(array(date_2)-array(date_1[i])) < datetime.timedelta(minutes=1))
			S = F[0]
			if len(S) > 0:
				util_1.append( date_1[i] )
				util_2.append( vector_1[i]+vector_2[S[0]] )
	else:
		for i in range(0,len(date_2)):
			F = numpy.where( abs(array(date_1)-array(date_2[i])) < datetime.timedelta(minutes=1))
			S = F[0]
			if len(S) > 0:
				util_1.append( date_2[i] )
				util_2.append( vector_1[S[0]]+vector_2[i] )
				
	return util_1,util_2
	
	

###--- DAY PRODUCTION ---###
def calculate_day_production(SP_datetime_inverter_N,SP_ene_inverter_N):

	#util to find min-max
	SP_utility_day_min           = []
	SP_utility_day_max           = []
	SP_utility_production_start  = []
	SP_utility_production_end    = []
	SP_utility_production        = []

	#select today - last available day
	lastday = max(SP_datetime_inverter_N)
	lastday = datetime.datetime(lastday.year,lastday.month,lastday.day,0,0,0)
	
	for i in range(0,len(SP_ene_inverter_N)):
		if SP_datetime_inverter_N[i] >= lastday:
			SP_utility_production.append(SP_ene_inverter_N[i])
	
	return max(SP_utility_production)-min(SP_utility_production)