# Date:			31-08-2012
# Purpose:      reading inverter data
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
###>>>
from read_csv_file import *
from day_production import *
### --- ###

#- -#

def reading_inverter_data(identifications,extension,folder):

	SP_datetime_inverter_1 = [];
	SP_ene_inverter_1      = [];
	SP_pow_inverter_1      = [];
	SP_datetime_dayproduction = []; SP_ene_dayproduction = [];

	#read Inverter data
	for root_dir, sub_dirs, files in os.walk(folder):
		SP_ene_loc1           = []
		SP_ene_loc2           = []	
		SP_datetime_local_1   = []
		SP_datetime_local_2   = []
		for file in files:
			check = 0
			file = string.lower(file)
			for identification in identifications:
 				if identification in file:
					check += 1
			if check == len(identifications) and os.path.splitext(file)[1] == extension:
   				SP_datetime_local_1 = read_csv_datetime(root_dir,file)
   				SP_ene_loc1         = read_csv_generic_column(root_dir,file,6)
   				SP_pow_inverter_1.extend(read_csv_generic_column(root_dir,file,5))

   				#---Correction inverter 1 Bianze'!!!
   				if 'inverter_1' in identifications: 
   					for c in range(0,len(SP_datetime_local_1)):
						if SP_datetime_local_1[c].date() >= datetime.date(2012,11,7):
  							if SP_datetime_local_1[c].date() <= datetime.date(2013,02,19):
								SP_ene_loc1[c]=SP_ene_loc1[c]+1079565
   				#---End correction inverter 1 Bianze'

				if len(SP_datetime_local_1) > 0:	
	 				SP_datetime_dayproduction.append(datetime.date(SP_datetime_local_1[0].year,SP_datetime_local_1[0].month,SP_datetime_local_1[0].day))
	 				SP_ene_dayproduction.append(calculate_day_production(SP_datetime_local_1,SP_ene_loc1))

				
		SP_datetime_inverter_1.extend(SP_datetime_local_1)
		SP_ene_inverter_1.extend(SP_ene_loc1)

	return SP_datetime_inverter_1, SP_ene_inverter_1, SP_pow_inverter_1, SP_datetime_dayproduction, SP_ene_dayproduction
