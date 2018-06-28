# Date:			17-07-2012
# Purpose:      check production and report errors
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
import math
### --- ###
from email_summary import *
### --- ###

def find_nearest_datetime(datetime,vector_datetime):
	F = abs(array(vector_datetime)-array(datetime))
	F = numpy.where( F == min(F) )
	if len(F[0])>0:
		return F[0][0]
	else:
		return float('nan')


def check_production(date_inverter,pow_inverter,date_pyranometer,pow_pyranometer,delta,expected_percentage):
	problem_list_datetime = []
	problem_list_pow      = []
	problem_list_expected = []

	for i in range(0,len(date_inverter)):
		F = find_nearest_datetime(date_inverter[i],date_pyranometer)
		if math.isnan(F) == False and abs(date_inverter[i]-date_pyranometer[F]) < delta:
			if pow_inverter[i] > 50. or pow_pyranometer[F] > 100.:
				if pow_inverter[i] < expected_percentage*pow_pyranometer[F]:
					problem_list_datetime.append(date_inverter[i])
					problem_list_pow.append(pow_inverter[i])
					problem_list_expected.append(expected_percentage*pow_pyranometer[F])
				
	return problem_list_datetime, problem_list_pow, problem_list_expected

#-comparison with pyranometer-#
def check_instant_production_1(date_inverter,pow_inverter,date_pyranometer,pow_pyranometer,delta,expected_percentage,first_failure,inverter_number,email_sent,email_addresses):

	print 'first_failure IN = ',first_failure
	#-verify proximity
	if len(date_pyranometer) > 0:
		F = find_nearest_datetime(date_inverter[len(date_inverter)-1],date_pyranometer)	
		if math.isnan(F) == False and abs(date_inverter[len(date_inverter)-1]-date_pyranometer[F]) < delta:
			if pow_pyranometer[F] > 100.:
				if pow_inverter[len(pow_inverter)-1] < expected_percentage*pow_pyranometer[F]:
					if len(first_failure) > 0:
						time_delta_failure = datetime.datetime.today()-first_failure[0]
						print time_delta_failure
						if  time_delta_failure > datetime.timedelta(hours=1) and email_sent == 0:
							email_sent = 1
							send_email_failure(inverter_number,email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(hours=3) and email_sent == 1:
							email_sent = 2
							send_email_failure(inverter_number,email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(days=1) and email_sent == 2:
							email_sent = 3
							send_email_failure(inverter_number,email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(days=2) and email_sent == 3:
							send_email_failure(inverter_number,email_sent,first_failure[0],email_addresses)
					else:
						first_failure = [date_inverter[len(date_inverter)-1]]
				else:
					first_failure = [] #-inver is back up
# 			else:
# 				first_failure = [] #-inver is going to sleep
	
	print 'first_failure = ',first_failure,'   email_sent = ',email_sent
	return first_failure, email_sent

#-inverter comparison-#
def check_instant_production_2(date_inverter_1,pow_inverter_1,date_inverter_2,pow_inverter_2,delta,expected_percentage,first_failure,email_sent,email_addresses):

	#-verify proximity
	if len(date_inverter_1) > 0:
		if abs(date_inverter_1[len(date_inverter_1)-1]-date_inverter_2[len(date_inverter_2)-1]) < delta:
			if pow_inverter_1[len(pow_inverter_1)-1] > 100.:
				if pow_inverter_1[len(pow_inverter_1)-1]/pow_inverter_2[len(pow_inverter_2)-1] < (1.0-expected_percentage) or pow_inverter_1[len(pow_inverter_1)-1]/pow_inverter_2[len(pow_inverter_2)-1] > (1.0+expected_percentage):
					if len(first_failure) > 0:
						time_delta_failure = datetime.datetime.today()-first_failure[0]
						if  time_delta_failure > datetime.timedelta(hours=1) and email_sent == 0:
							email_sent = 1
							send_email_failure_inverters(email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(hours=3) and email_sent == 1:
							email_sent = 2
							send_email_failure_inverters(email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(days=1) and email_sent == 2:
							email_sent = 3
							send_email_failure_inverters(email_sent,first_failure[0],email_addresses)
						elif time_delta_failure > datetime.timedelta(days=2) and email_sent == 3:
							send_email_failure_inverters(email_sent,first_failure[0],email_addresses)
					else:
						first_failure = [date_inverter_1[len(date_inverter_1)-1]]
				else:
					first_failure = [] #-inver is back up
# 			else:
# 				first_failure = [] #-inver is going to sleep
	
	print 'first_failure = ',first_failure,'   email_sent = ',email_sent
	return first_failure, email_sent
