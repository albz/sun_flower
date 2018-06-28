# Date:			02-02-2012
# Purpose:      year production subroutines
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



###--- YEAR SEQUENTIAL PRODUCTION ---###
def calculate_yearly_production(SP_datetime_inverter_N,SP_ene_inverter_N):


	#util to find min-max
	SP_utility_year_min          = []
	SP_utility_year_max          = []
	SP_utility_production_start  = []
	SP_utility_production_end    = []

	SP_ene_yearproduction       = []
	SP_datetime_yearproduction  = []


	day_zero   = min(SP_datetime_inverter_N); 
	year_zero  = day_zero.year; 
	month_zero = day_zero.month; 
	day_zero   = day_zero.day

	#select the maximum and the minimum for each year
	l = len(SP_datetime_inverter_N)
	dimension_year = 1
	for i in range(0,l):
		y       = SP_datetime_inverter_N[i].year - year_zero
		dimension_year = max(y,dimension_year)

	for i in range(0,dimension_year+1):
		SP_utility_year_max.append( datetime.datetime(1000,1,1,0,0,0) )
		SP_utility_year_min.append( datetime.datetime(3000,1,1,0,0,0) )
		SP_utility_production_start.append(0)
		SP_utility_production_end.append(0)

	for i in range(0,l):
 		y       = SP_datetime_inverter_N[i].year - year_zero
 		if SP_datetime_inverter_N[i] > SP_utility_year_max[y]:
 			SP_utility_year_max[y]        = SP_datetime_inverter_N[i]
 			SP_utility_production_end[y]   = SP_ene_inverter_N[i]
 		if SP_datetime_inverter_N[i] < SP_utility_year_min[y]:
 			SP_utility_year_min[y]        = SP_datetime_inverter_N[i]
 			SP_utility_production_start[y] = SP_ene_inverter_N[i]
	
	for i in range(0,dimension_year+1):
 		y       = SP_utility_year_min[i].year
		SP_datetime_yearproduction.append( datetime.date(y,1,1) )
		SP_ene_yearproduction.append( SP_utility_production_end[i] - SP_utility_production_start[i] )


	return SP_datetime_yearproduction,SP_ene_yearproduction