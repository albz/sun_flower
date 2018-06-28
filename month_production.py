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



###--- MONTLY SEQUENTIAL PRODUCTION ---###
def calculate_montly_production(SP_datetime_inverter_N,SP_ene_inverter_N):


	#util to find min-max
	SP_utility_month_min         = []
	SP_utility_month_max         = []
	SP_utility_production_start  = []
	SP_utility_production_end    = []

	SP_ene_monthproduction       = []
	SP_datetime_monthproduction  = []


	day_zero   = min(SP_datetime_inverter_N); 
	year_zero  = day_zero.year; 
	month_zero = day_zero.month; 
	day_zero   = day_zero.day

	#select the maximum and the minimum for each month
	l = len(SP_datetime_inverter_N)
	dimension_month = 1; dimension_year = 1;
	for i in range(0,l):
		y       = SP_datetime_inverter_N[i].year
		m       = SP_datetime_inverter_N[i].month
	
		month_counter = (y-year_zero)*12 + (m-month_zero)
		dimension_month = max(month_counter,dimension_month)

	for i in range(0,dimension_month+1):
		SP_utility_month_max.append( datetime.datetime(1000,1,1,0,0,0) )
		SP_utility_month_min.append( datetime.datetime(3000,1,1,0,0,0) )
		SP_utility_production_start.append(0)
		SP_utility_production_end.append(0)

	for i in range(0,l):
 		y       = SP_datetime_inverter_N[i].year
 		m       = SP_datetime_inverter_N[i].month
 		m       = (y-year_zero)*12 + (m-month_zero)
 		if SP_datetime_inverter_N[i] > SP_utility_month_max[m]:
 			SP_utility_month_max[m]        = SP_datetime_inverter_N[i]
 			SP_utility_production_end[m]   = SP_ene_inverter_N[i]
 		if SP_datetime_inverter_N[i] < SP_utility_month_min[m]:
 			SP_utility_month_min[m]        = SP_datetime_inverter_N[i]
 			SP_utility_production_start[m] = SP_ene_inverter_N[i]
	
	for i in range(0,dimension_month+1):
 		y       = SP_utility_month_min[i].year
 		m       = SP_utility_month_min[i].month
		SP_datetime_monthproduction.append( datetime.date(y,m,1) )
		SP_ene_monthproduction.append( SP_utility_production_end[i] - SP_utility_production_start[i] )

	return SP_datetime_monthproduction,SP_ene_monthproduction






###--- MONTLY CORRELATED PRODUCTION ---###
def calculate_montly_correlated_production(SP_datetime,SP_ene):

	
	#select matrix dimensions
	day_zero   = min(SP_datetime); 
	year_zero  = day_zero.year; 
	month_zero = day_zero.month; 
	day_zero   = day_zero.day
	
	l = len(SP_datetime)
	dimension_year = 1;
	for i in range(0,l):
		y       = SP_datetime[i].year
		year_counter = (y-year_zero)
		dimension_year = max(year_counter,dimension_year)

	montly_correlated_matrix = zeros([12,dimension_year+1])
	
	for i in range(0,l):
		y       = SP_datetime[i].year  - year_zero
		m       = SP_datetime[i].month

 		montly_correlated_matrix[m-1,y] = SP_ene[y*12 + (m-month_zero)]
		
	return montly_correlated_matrix
