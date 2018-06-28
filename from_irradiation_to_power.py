# Date:			02-02-2012
# Purpose:      from solar irradiation to power produced by solar modules
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string, random
import time,datetime
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
from dateutil.relativedelta import relativedelta
###>>>
from read_csv_file import *
### --- ###


#time format
#time_format = "%Y-%m-%d %H:%M:%S"

#one day delta
one_day   = datetime.timedelta(days=1)


###--- MODEL TO GIVE INTENSITY IN FUNCTION OF VOLTAGE-IRRADIATION-TEMPERATURE ---###
def solar(Va,irradiance,TaC):

 	Va  = array(Va)
 	TaC = TaC * 1.0
	
	Suns = irradiance / 1000.0 #defining G
	
	k = 1.38e-23 #Boltzmann Constants
	q = 1.60e-19 #e-charge
	
	n  = 2.0    #diode quality, n=2 christal, <2 amorfo
	Vg = 1.12   #voltage bandwith, 1.12 christal, 1.75 Si amorfo
	Ns = 36     #diode cells
	
	T1 = 273. + 25.
	Voc_T1 = 21.06 /Ns
	Isc_T1 = 3.80
	T2 = 273. + 75.
	Voc_T2 = 17.05 /Ns
	Isc_T2 = 3.92
	
	TaK = 273. + TaC
	K0 = (Isc_T2 - Isc_T1)/(T2 - T1)
	IL_T1 = Isc_T1 * Suns
	IL = IL_T1 + K0*(TaK - T1)
	I0_T1=Isc_T1/(exp(q*Voc_T1/(n*k*T1))-1)
	I0= I0_T1 * numpy.power(TaK/T1,3/n) * exp(-q*Vg/(n*k) * ((1./TaK)-(1./T1)))
	Xv = I0_T1*q/(n*k*T1) * exp(q*Voc_T1/(n*k*T1))
	dVdI_Voc = - 1.15/Ns / 2.0
	
	Rs = - dVdI_Voc - 1./Xv
	A = 3.9-0.5*(Suns-0.2)
	#A = 3.5
	Vt_Ta = A * k * TaK / q
	Vc = Va/Ns
	Ia = zeros(Vc.shape[0])
	
	for j in range(0,5):
		Ia = Ia- (IL-Ia - I0*( exp((Vc+Ia*Rs)/Vt_Ta) -1)) / (-1. - (I0*( exp((Vc+Ia*Rs)/Vt_Ta) -1.))*Rs/Vt_Ta);
	
	Ia = Ia*2.25;
		
	return Ia
	
	
	
###--- using the above MODEL estimation of maximum power ---###	
def irr_to_power(irradiance,TaC):	
	
	max_power = []
	
	irradiance = array(irradiance)
	TaC        = array(TaC)
	
	Va = arange(15.0,32.0,0.2)

	for i in range(0,irradiance.shape[0]):
		Ia = solar(Va,irradiance[i],TaC[i])
		max_power.append(max(Va*Ia))

	return max_power



###--- CALCULATE DELTA OF TIME IN HRS ---###
def time_delta_hrs(date1,date2):
	
	s1 = date1.hour*3600.0 + date1.minute*60.0 + date1.second*1.0
	s2 = date2.hour*3600.0 + date2.minute*60.0 + date2.second*1.0
	
	return abs(s2-s1)/3600.0


###--- INTEGRATION=>ENERGY for a day: TRAPEZOIDAL RULE ---###
def integration_energy_day(date,irradiance,TaC):
	
	pow = irr_to_power(irradiance,TaC)
	pow = array(pow) * 4340.0/1e3
		
	Energy_day = 0.0
	for i in range(0,len(irradiance)-1):
		Energy_day += 0.5 * (pow[i]+pow[i+1])*(time_delta_hrs(date[i],date[i+1]))
	
	return pow, Energy_day


###--- adding with few statistical rules the missing production or not aquisition dates ---###
def statistics_to_add_missing_production(date,energy):

 	date_no_gap = []; energy_no_gap = [];

	start_date = min(date)
	counter    = start_date
	i          = 0

	#--statistic utility--#
	n           = (datetime.date.today().year-start_date.year)*12 + (datetime.date.today().month-start_date.month)
	mean_matrix = ones( (n+1,31) ) * -1.0
	#-- --#

	while counter <= datetime.date.today():
		for k in range(0,len(energy)):
			if counter == date[k]:
				#-I do generate the statistic in here-#
				m = (counter.year-start_date.year)*12 + (counter.month-start_date.month)
				mean_matrix[m,counter.day-1] = energy[k]
				#- -#
				date_no_gap.append(counter)
				energy_no_gap.append(energy[k])
# 				print 'energy > ',counter,energy[k],k
				break
		else:
			date_no_gap.append(counter)
			energy_no_gap.append(0.0)
		counter += datetime.timedelta(days=1)
		
 	mean_matrix = numpy.ma.masked_array( mean_matrix, mask=mean_matrix<=0 )
 	SP_mean     = mean( mean_matrix, axis=1)
 	SP_std      = std(  mean_matrix, axis=1)

	for i in range(0,len(energy_no_gap)):
		if energy_no_gap[i] == 0.0:
			m                = (date_no_gap[i].year-start_date.year)*12 + (date_no_gap[i].month-start_date.month)
			if m <= len(SP_mean)-2:
				energy_estimat   = normal(SP_mean[m], SP_std[m],1)[0]
			else:
				energy_estimat = 0.0
			while energy_estimat < 0:
				energy_estimat = normal(SP_mean[m], SP_std[m],1)[0]
			energy_no_gap[i] = energy_estimat
	
	return date_no_gap,energy_no_gap



###--- CALCULATE PREDICTED ENERGY FROM PYRANOMETER ---###
def energy_pyranometer_extimation(folder):

	SP_expected_energy_day   = []; 	SP_expected_datetime_day    = []; 
	SP_expected_energy_month = [];	SP_expected_datetime_month  = [];
	SP_expected_energy_year  = [];	SP_expected_datetime_year   = [];
	SP_pow_total             = [];  SP_datetime_total           = [];
	date_no_gap              = [];  energy_no_gap               = [];
	pow                      = [];
	year_zero = -1; month_zero = -1;
	
	#read pyronometer data
	for root_dir, sub_dirs, files in os.walk(folder):
		for file in files:
			file = string.lower(file)
			SP_datetime_solarimetro = []; SP_irr = []; SP_temperature = [];

			if 'solarimetro' in file and os.path.splitext(file)[1] == '.csv':
				SP_datetime_solarimetro = read_csv_datetime(root_dir,file)
				SP_irr                  = read_csv_generic_column(root_dir,file,2)
				SP_temperature          = read_csv_generic_column(root_dir,file,3)
				
				if len(SP_datetime_solarimetro) > 1:

					pow = []; energy=[];
					pow,energy  = integration_energy_day(SP_datetime_solarimetro,SP_irr,SP_temperature)
				
					SP_pow_total.extend(pow)
					SP_datetime_total.extend(SP_datetime_solarimetro)
				
					SP_expected_energy_day.append(energy)
					y       = SP_datetime_solarimetro[0].year; 
					m       = SP_datetime_solarimetro[0].month
 					d       = SP_datetime_solarimetro[0].day
					SP_expected_datetime_day.append(datetime.date(y,m,d))
					
	#- adding with statistics the missing dates
	date_no_gap,energy_no_gap = statistics_to_add_missing_production(SP_expected_datetime_day,SP_expected_energy_day)
 	SP_expected_datetime_day  = date_no_gap
 	SP_expected_energy_day    = energy_no_gap

	#- I do not like this part, but it should be quicker -#
	#- now filling Month vectors -#
	date_zero = min(date_no_gap)
	date_last = max(date_no_gap)
	incremental_date = date_zero
	i = 0
	while incremental_date <= date_last:
		
		y = incremental_date.year
		m = incremental_date.month
		
				#- now filling Month vectors -#
		month = (incremental_date.year-date_zero.year)*12 + (incremental_date.month-date_zero.month)
		if month > len(SP_expected_datetime_month)-1:
			SP_expected_datetime_month.append(datetime.date(y,m,1))
			SP_expected_energy_month.append(energy_no_gap[i])
		else:
			SP_expected_energy_month[month] += energy_no_gap[i]

				#- now filling Years vectors -#
		year = incremental_date.year-date_zero.year
		if year > len(SP_expected_datetime_year)-1:
			SP_expected_datetime_year.append(datetime.date(y,m,1))
			SP_expected_energy_year.append(energy_no_gap[i])
		else:
			SP_expected_energy_year[year] += energy_no_gap[i]

		incremental_date += one_day
		i += 1

	return 	SP_datetime_total,SP_pow_total,SP_expected_datetime_day,SP_expected_energy_day,SP_expected_datetime_month,SP_expected_energy_month,SP_expected_datetime_year,SP_expected_energy_year