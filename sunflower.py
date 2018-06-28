#!/usr/bin/python
######################################################################
# Name:         sunflower
# Date:			02-02-2012
# Purpose:      Albz's solar power plant analysis python script
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string, ftplib
import time, datetime, math, getpass
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
###>>>
sys.path.append(os.path.split(os.getcwd())[0])
###>>>
from read_csv_file import *
from day_production import *
from month_production import *
from year_production import *
from plot_subroutines import *
from from_irradiation_to_power import *
from synch_tool import *
from email_summary import *
from check_production import *
from print_and_read_analyzed_data_on_file import *
from read_inverter_data import *
from copy_data_to_dropbox import *
from program_input_control import *
### --- ###


#- program inputs -#
#-graphing style-#
					# if input 0 == 'display' ==> 0 - display
					# if input 0 == 'print'   ==> 1 - print on file
					# if input 1 == 'loop'    ==> loop = True
					# if input 1 == 'noloop'  ==> loop = False
graph_style, loop = input_control_parameters(sys.argv[1:])
#- -#

#- remote access -#
port = 21
username = '------------'
password = '------------'
host     = '001.001.001.001'
#- -#

#paths
path                   = os.getcwd()
folder                 = os.path.join(path,'data')
folder_images          = os.path.join(path,'images')
drop_box_folder_data   = os.path.join(os.path.join('/Volumes/Macintosh_HD/Users',getpass.getuser()),'Dropbox/fotovoltaico/A/data')
drop_box_folder_images = os.path.join(os.path.join('/Volumes/Macintosh_HD/Users',getpass.getuser()),'Dropbox/fotovoltaico/A/images')
#- -#

#-emails-#
email_addresses_summary       = ['a.b@gmail.com','a.b@gmail.com']
email_addresses_report_errors = ['a.b@gmail.com','a.b@gmail.com']
#- -#

#time format
time_format = "%Y-%m-%d %H:%M:%S"

#day to analyze
day_to_analyze = datetime.datetime(2011,9,11,0,0,0)
one_day        = datetime.timedelta(days=1)
delta_1        = datetime.timedelta(minutes=3)
delta_2        = datetime.timedelta(minutes=30)

#PVGIS - values
#PVGIS=[77600.00,78300.00,123000.00,124000.00,130000.00,142000.00,155000.00,150000.00,129000.00,99500.00,72900.00,65500.00]
PVGIS=[61900.00,63800.00,102000.00,105300.00,112000.00,124000.00,135000.00,126000.00,108000.00,81600.00,58500.00,51900.00]

#util
SP_ene_dayproduction      = [];
SP_datetime_dayproduction = [];

SP_ene_monthproduction      = [];
SP_datetime_monthproduction = [];

SP_ene_yearproduction      = [];
SP_datetime_yearproduction = [];
#- -#
failure_1 = []; failure_2 = []; failure_3 = []
email_sent_1 = 0; email_sent_2 = 0; email_sent_3 = 0
#- -#

#- -#
deadline = datetime.datetime(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day,22,0,0)
#- -#



while 1 > 0:   #-- infinity analysis loop

	###---> SYNC FILES
	start_import_date = find_start_import_date(folder)
	print '>',start_import_date
	import_data(start_import_date,folder,username,password,host,port)
	###--->

	### ### ### ### ### ### ### ### ### ###

	###--- READING INVERTER DATA ---###
	SP_datetime_inverter_1, SP_ene_inverter_1, SP_pow_inverter_1, SP_datetime_dayproduction_1, SP_ene_dayproduction_1 = reading_inverter_data(['inverter_1','pannello_controllo_inverter'],'.csv',folder)
	SP_datetime_inverter_2, SP_ene_inverter_2, SP_pow_inverter_2, SP_datetime_dayproduction_2, SP_ene_dayproduction_2 = reading_inverter_data(['inverter_2','pannello_controllo_inverter'],'.csv',folder)

	SP_datetime_dayproduction, SP_ene_dayproduction = sum_date_vectors(SP_datetime_dayproduction_1,SP_ene_dayproduction_1,SP_datetime_dayproduction_2,SP_ene_dayproduction_2)
	###########################################

	###--- ENERGY ESTIMATION VIA PYRANOMETER ---###
	SP_datetime_solarimetro,SP_irr,SP_expected_datetime_day,SP_expected_energy_day,SP_expected_datetime_month,SP_expected_energy_month,SP_expected_datetime_year,SP_expected_energy_year = energy_pyranometer_extimation(folder)
	###########################################


	###########################################
	###--- SELECT DAY ---###
	today = datetime.date.today()
	today = max(SP_datetime_dayproduction)
	day_to_analyze = datetime.datetime(today.year,today.month,today.day,0,0,0)
	#day_to_analyze = datetime.datetime(2014,4,17,0,0,0)
	util_1=[]; util_2=[]
	util_3=[]; util_4=[]
	util_5=[]; util_6=[]
	util_7=[]; util_8=[]
	util_9=[]; util_10=[]
	util_11=[];util_12=[]

	util_1,util_2 = selected_day(SP_datetime_inverter_1,SP_pow_inverter_1,day_to_analyze)
	util_3,util_4 = selected_day(SP_datetime_inverter_2,SP_pow_inverter_2,day_to_analyze)
	util_5,util_6 = sum_datetime_vectors(util_1,util_2,util_3,util_4,delta_1)

	util_7,util_8 = selected_day(SP_datetime_solarimetro,SP_irr,day_to_analyze)

	#plot_pow_vs_expected_with_inverter_detached(util_5,util_6,util_7,util_8,util_1,util_2,util_3,util_4,graph_style,folder_images)
	### end selected day
	###########################################

	###########################################
	###--->>> *PROBLEM ANALYSIS!* <<<---###
	###--- last available day, from previous section ---###
# 	print 'email sent check = ',email_sent_1,email_sent_2
	inverter_number = 1
# 	print util_1
# 	print util_7
# 	print util_2
# 	print util_8
	failure_1, email_sent_1 = check_instant_production_1(util_1,util_2,util_7,util_8,delta_2,0.47,failure_1,inverter_number,email_sent_1,email_addresses_report_errors)

	inverter_number = 2
	failure_2, email_sent_2 = check_instant_production_1(util_3,util_4,util_7,util_8,delta_2,0.47,failure_2,inverter_number,email_sent_2,email_addresses_report_errors)
# 	print 'email sent check *dopo*= ',email_sent_1,email_sent_2

	failure_3, email_sent_3 = check_instant_production_2(util_1,util_2,util_3,util_4,delta_1,0.03,failure_3,email_sent_3,email_addresses_report_errors)

	### end problem analysis
	###########################################


	#>>>
	if loop == False or datetime.datetime.today() >= deadline:
		###--- ---###
		if loop == True:
			deadline += one_day
		###--- ---###


		###--- SELECTED DAY ---###
		plot_pow_vs_expected_with_inverter_detached(util_5,util_6,util_7,util_8,util_1,util_2,util_3,util_4,graph_style,folder_images)
		###--- end selected day

		###--- DAYLY PRODUCTION SINCE ZERO TIME ---###
		daily_production_plus_thestimation_plot(SP_datetime_dayproduction,SP_ene_dayproduction,SP_expected_datetime_day,SP_expected_energy_day,datetime.timedelta(days=7),graph_style,folder_images)
		daily_production_plus_thestimation_plot(SP_datetime_dayproduction,SP_ene_dayproduction,SP_expected_datetime_day,SP_expected_energy_day,datetime.timedelta(days=30),graph_style,folder_images)
		daily_production_plus_thestimation_plot(SP_datetime_dayproduction,SP_ene_dayproduction,SP_expected_datetime_day,SP_expected_energy_day,0,graph_style,folder_images)
		###--- end dayly-production-since-zero-time

		###--- VERIFY PRODUCTION INVERTERS-EXTIMATION ---###
		###--- last available day, from previous section ---###
		problem_list_datetime_1, problem_list_pow_1, problem_list_expected_1 = check_production(util_1,util_2,util_7,util_8,delta_2,0.45)
		problem_list_datetime_2, problem_list_pow_2, problem_list_expected_2 = check_production(util_3,util_4,util_7,util_8,delta_2,0.45)

		l_1 = len(problem_list_datetime_1)
		l_2 = len(problem_list_datetime_2)
		error_matrix = [[0 for x in xrange(4)] for x in xrange(l_1+l_2)]
		for i in range(0,l_1):
			error_matrix[i][0]=problem_list_datetime_1[i]
			error_matrix[i][1]=problem_list_pow_1[i]
			error_matrix[i][2]=problem_list_expected_1[i]
			error_matrix[i][3]=1

		for i in range(0,l_2):
			error_matrix[i+l_1][0]=problem_list_datetime_2[i]
			error_matrix[i+l_1][1]=problem_list_pow_2[i]
			error_matrix[i+l_1][2]=problem_list_expected_2[i]
			error_matrix[i+l_1][3]=2
		# ### end verification

		###--- MONTLY SEQUENTIAL PRODUCTION ---###
		util_1=[]; util_2=[]
		util_3=[]; util_4=[]

		util_1,util_2 = calculate_montly_production(SP_datetime_inverter_1,SP_ene_inverter_1)
		util_3,util_4 = calculate_montly_production(SP_datetime_inverter_2,SP_ene_inverter_2)

		SP_ene_monthproduction       = array(util_2) + array(util_4)
		SP_datetime_monthproduction  = util_1

		PVGIS_equivalent = []
		for i in range(0,len(SP_datetime_monthproduction)):
			PVGIS_equivalent.append( PVGIS[SP_datetime_monthproduction[i].month-1] )

		montly_sequential_plus_thestimation_plot(SP_datetime_monthproduction,SP_ene_monthproduction,PVGIS_equivalent,SP_expected_datetime_month,SP_expected_energy_month,graph_style,folder_images)
		### --->>> end montly sequential production

		###--- MONTLY CORRELATED PRODUCTION ---###
		SP_ene_monthproduction_correlated = calculate_montly_correlated_production(SP_datetime_monthproduction,SP_ene_monthproduction)
		montly_correlated_plot(SP_ene_monthproduction_correlated,PVGIS,graph_style,folder_images)
		### --->>> end montly correlated production

		###--- YEAR SEQUENTIAL PRODUCTION ---###
		util_1=[]; util_2=[]
		util_3=[]; util_4=[]

		util_1,util_2  = calculate_yearly_production(SP_datetime_inverter_1,SP_ene_inverter_1)
		util_3,util_4  = calculate_yearly_production(SP_datetime_inverter_2,SP_ene_inverter_2)

		SP_ene_yearproduction      = array(util_2) + array(util_4)
		SP_datetime_yearproduction = util_1

		yearly_sequential_plot(SP_datetime_yearproduction,SP_ene_yearproduction,sum(PVGIS),graph_style,folder_images)
		### --->>> end montly correlated production


		###--- Utility Graph - DailyPower VS time ---###
		plot_DayPower_vs_Time([SP_datetime_inverter_1,SP_datetime_inverter_2],[SP_pow_inverter_1,SP_pow_inverter_2],graph_style,folder_images)
		### --->>> End Graph - DailyPower VS time


		###--- Send e-mail with report ---###
		today_statistic      = [calculate_day_production(SP_datetime_inverter_1,SP_ene_inverter_1)+calculate_day_production(SP_datetime_inverter_2,SP_ene_inverter_2),SP_expected_energy_day[len(SP_expected_energy_day)-1],PVGIS[datetime.date.today().month-1]/30.]
		this_month_statistic = [SP_ene_monthproduction[len(SP_ene_monthproduction)-1],SP_expected_energy_month[len(SP_expected_energy_month)-1],PVGIS_equivalent[len(PVGIS_equivalent)-1]]
		this_year_statistic  = [SP_ene_yearproduction[len(SP_ene_yearproduction)-1],sum(PVGIS)]
		send_email(today_statistic,this_month_statistic,this_year_statistic,error_matrix,email_addresses_summary,folder_images)
		###print this_month_statistic
		###########################################

		###--- copy data to DropBox ---###
		copy_data_to_dropbox(folder,drop_box_folder_data)          #data
		copy_data_to_dropbox(folder_images,drop_box_folder_images) #images
		###--- ---###



	###--- File synch writing last updated date ---###
	day_to_write = max(SP_datetime_dayproduction) - datetime.timedelta(days=1)
	write_last_day_analized(day_to_write,folder)
	###--- ---###

	###---###
	if loop == False:
		sys.exit()
	if loop == True:
		time.sleep(600)
	###---###
